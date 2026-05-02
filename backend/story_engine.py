import os
from typing import List, Dict, Tuple, Optional

from narrators import NARRATOR_PROFILES, compute_mood_shift, describe_mood
from world_state import compute_world_state, compute_drift_signature, get_conditional_choices
from adventure_registry import get_adventure, get_premise, resolve_choice

_api_key: Optional[str] = os.environ.get("ANTHROPIC_API_KEY")
_client = None

_gemini_api_key: Optional[str] = os.environ.get("GEMINI_API_KEY")
_gemini_client = None


def _get_client():
    global _client
    if _client is None and _api_key:
        import anthropic
        _client = anthropic.Anthropic(api_key=_api_key)
    return _client


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None and _gemini_api_key:
        from google import genai
        _gemini_client = genai.Client(api_key=_gemini_api_key)
    return _gemini_client


# ---------------------------------------------------------------------------
# History utilities
# ---------------------------------------------------------------------------

def summarize_history(history: list) -> str:
    if not history:
        return "No prior choices."
    recent = history[-4:]
    parts = [f"chose '{h.get('player_choice', '?')}'" for h in recent]
    return "Player recently " + ", then ".join(parts) + "."


def extract_narrator_memory(
    history: list,
    session_count: int,
    landmarks: dict,
    mood: dict = None,
    drift_signature: str = None,
) -> str:
    if not history and session_count <= 1:
        return ""
    visited = {h.get("beat_id") for h in history}
    found = [desc for beat_id, desc in landmarks.items() if beat_id in visited]
    parts = []
    if session_count > 1:
        n = session_count
        suffix = "rd" if n == 3 else "th" if n > 3 else "nd"
        parts.append(f"This is the player's {n}{suffix} run.")
    if found:
        parts.append("They previously: " + ", ".join(found) + ".")
    if mood:
        dominant = max(mood, key=mood.get)
        if mood[dominant] > 0.5:
            arc_labels = {
                "trust":      "growing trust",
                "suspicion":  "rising suspicion",
                "curiosity":  "keen curiosity",
            }
            parts.append(f"The player has shown {arc_labels[dominant]} throughout.")
    if drift_signature and drift_signature != "The Drifter":
        parts.append(f"They carry the mark of {drift_signature}.")
    if parts:
        parts.append("The narrator remembers.")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Static beat generation (no API key)
# ---------------------------------------------------------------------------

def get_static_beat(node: dict, narrator_name: str, narrator_profile: dict) -> str:
    base = node.get("text", "")
    tone = node.get("tone", "")
    flavor_lines = narrator_profile.get("flavor_lines", {})
    flavor = flavor_lines.get(tone, "")
    if flavor:
        return base + " " + flavor
    return base


# ---------------------------------------------------------------------------
# LLM beat generation
# ---------------------------------------------------------------------------

def generate_beat_with_llm(
    scene_prompt: str,
    static_text: str,
    node: dict,
    narrator_profile: dict,
    history_summary: str,
    player_choice: str,
    mood: dict,
    history: list,
    session_count: int,
    drift_signature: str,
    narrator_memory: str,
) -> str:
    client = _get_client()

    if client is None:
        return get_static_beat(node, narrator_profile["name"], narrator_profile)

    mood_desc = describe_mood(mood)
    tone = node.get("tone", "")

    system_parts = [
        f"You are {narrator_profile['name']}, a narrator in an interactive story.",
        f"Tone: {narrator_profile['tone']}",
        f"Behavior: {narrator_profile['behavior']}",
        f"Current emotional state toward the player: {mood_desc}",
        f"Drift Signature: {drift_signature}",
    ]
    if tone:
        system_parts.append(f"This beat's emotional tone: {tone}")
    if narrator_memory:
        system_parts.append(f"Memory: {narrator_memory}")
    system_parts.append(
        "\nWrite a single vivid narrative beat: 2–4 sentences, present tense. "
        "No bullet points. No choice prompts. No questions. "
        "Stay entirely in your narrator voice. End on an atmospheric note."
    )
    system = "\n".join(system_parts)

    user = (
        f"Scene context: {scene_prompt}\n"
        f"Player's last action: \"{player_choice}\"\n"
        f"Story so far: {history_summary}\n\n"
        f"Write the next beat as {narrator_profile['name']}."
    )

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=350,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text.strip()


# ---------------------------------------------------------------------------
# Open-ended session generation
# ---------------------------------------------------------------------------

_ARC_PHASES = [
    (3,  "setup",       "Establish the setting and situation. Introduce the core tension."),
    (12, "exploration", "Deepen the mystery. Let the player discover and react. Raise the stakes."),
    (999,"resolution",  "Drive toward a conclusion. The player's choices should feel consequential now."),
]


def _get_arc_phase(beat_count: int) -> Tuple[str, str]:
    for threshold, name, guidance in _ARC_PHASES:
        if beat_count <= threshold:
            return name, guidance
    return "resolution", _ARC_PHASES[-1][2]


def generate_open_beat(
    premise: dict,
    narrator_profile: dict,
    history: list,
    player_choice: str,
    mood: dict,
    drift_signature: str,
    session_count: int,
) -> Tuple[str, List[str], bool]:
    """
    For open-ended (AI DM) sessions.
    Returns (beat_text, choices_list, rng_triggered=False).
    Requires ANTHROPIC_API_KEY.
    """
    try:
        gemini = _get_gemini_client()
        if gemini is None:
            return (
                "The narrator is unavailable for open drifts without a Gemini API key. "
                "Choose a guided tale from the menu.",
                ["return to adventures"],
                False,
            )

        beat_count = len(history)
        arc_phase, arc_guidance = _get_arc_phase(beat_count)
        mood_desc = describe_mood(mood)
        history_summary = summarize_history(history)

        system = (
            f"You are {narrator_profile['name']}, acting as a narrator and game master "
            f"for an interactive story session.\n"
            f"Setting: {premise['title']} — {premise['description']}\n"
            f"Arc guidance: {premise['arc_hint']}\n"
            f"Current phase: {arc_phase}. {arc_guidance}\n"
            f"Narrator tone: {narrator_profile['tone']}\n"
            f"Narrator behavior: {narrator_profile['behavior']}\n"
            f"Emotional state toward player: {mood_desc}\n"
            f"Drift Signature: {drift_signature}\n\n"
            "Write a narrative beat (3–5 sentences, present tense) that advances the story. "
            "Then provide EXACTLY 3 choices the player can make, formatted as:\n"
            "CHOICES:\n- choice one\n- choice two\n- choice three\n\n"
            "Choices should be specific, meaningful, and reflect real options in this situation. "
            "Do not number them. Do not add explanations."
        )

        user = (
            f"Player's last action: \"{player_choice}\"\n"
            f"Story so far: {history_summary}\n\n"
            "Write the next beat and choices."
        )

        from google.genai import types
        response = gemini.models.generate_content(
            model="gemini-2.0-flash",
            contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system,
                max_output_tokens=500,
            ),
        )
        raw = response.text.strip()
    except Exception as e:
        return (
            f"[Gemini error — {type(e).__name__}: {e}]",
            ["try again", "return to adventures"],
            False,
        )

    # Parse beat and choices
    if "CHOICES:" in raw:
        parts = raw.split("CHOICES:", 1)
        beat_text = parts[0].strip()
        choices_raw = parts[1].strip()
        choices = [
            line.lstrip("- •").strip()
            for line in choices_raw.split("\n")
            if line.strip() and line.strip() not in ("", "-")
        ][:3]
    else:
        beat_text = raw
        choices = ["continue", "look around", "hold back"]

    if not choices:
        choices = ["continue", "look around", "hold back"]

    return beat_text, choices, False


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def generate_next_beat(
    history: List[Dict],
    player_choice: str,
    narrator: str,
    current_beat_id: str = "intro",
    session_count: int = 1,
    adventure_id: str = "last_voicemail",
    adventure_type: str = "guided",
    premise_id: Optional[str] = None,
) -> Tuple[str, List[str], str, Dict, str, bool]:
    """
    Returns (beat_text, choices, next_beat_id, mood, drift_signature, rng_triggered).
    Handles guided tales (story graph) and open-ended (AI DM) sessions.
    """
    mood = compute_mood_shift(history)
    world_state = compute_world_state(history, session_count)
    drift_signature = compute_drift_signature(world_state, mood)
    narrator_profile = NARRATOR_PROFILES.get(narrator, NARRATOR_PROFILES["The Whisperer"])

    # ── Open-ended mode ──────────────────────────────────────────────────────
    if adventure_type == "open":
        pid = premise_id or adventure_id
        premise = get_premise(pid) or {
            "title": "Unknown Setting",
            "description": "An open world.",
            "arc_hint": "Explore freely.",
        }
        beat_text, choices, rng = generate_open_beat(
            premise=premise,
            narrator_profile=narrator_profile,
            history=history,
            player_choice=player_choice,
            mood=mood,
            drift_signature=drift_signature,
            session_count=session_count,
        )
        return beat_text, choices, current_beat_id, mood, drift_signature, rng

    # ── Guided mode ──────────────────────────────────────────────────────────
    adventure = get_adventure(adventure_id)
    if adventure is None:
        adventure = get_adventure("last_voicemail")

    graph = adventure["graph"]
    landmarks = adventure["landmarks"]

    node = graph.get(current_beat_id, graph.get("intro", {}))

    # "start" means: read the current node itself, don't advance
    if player_choice == "start":
        next_beat_id = current_beat_id
        next_node = node
        rng_triggered = False
    else:
        next_beat_id, rng_triggered = resolve_choice(node, player_choice)
        next_node = graph.get(next_beat_id, graph.get("intro", {}))

    if adventure.get("meta", {}).get("use_authored_text"):
        beat_text = next_node.get("text", "")
        display_choices = list(next_node.get("choices", {}).keys())
        for choice_text, _ in get_conditional_choices(next_node, world_state, mood):
            if choice_text not in display_choices:
                display_choices.append(choice_text)
        return beat_text, display_choices, next_beat_id, mood, drift_signature, rng_triggered

    narrator_memory = extract_narrator_memory(history, session_count, landmarks, mood=mood, drift_signature=drift_signature)
    history_summary = summarize_history(history)

    beat_text = generate_beat_with_llm(
        scene_prompt=next_node.get("scene_prompt", ""),
        static_text=next_node.get("text", ""),
        node=next_node,
        narrator_profile=narrator_profile,
        history_summary=history_summary,
        player_choice=player_choice,
        mood=mood,
        history=history,
        session_count=session_count,
        drift_signature=drift_signature,
        narrator_memory=narrator_memory,
    )

    # Build display choices for next node
    raw_choices = next_node.get("choices", {})
    display_choices = list(raw_choices.keys())
    for choice_text, _ in get_conditional_choices(next_node, world_state, mood):
        if choice_text not in display_choices:
            display_choices.append(choice_text)

    return beat_text, display_choices, next_beat_id, mood, drift_signature, rng_triggered
