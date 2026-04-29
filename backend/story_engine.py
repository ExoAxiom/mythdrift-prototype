import os
from typing import List, Dict, Tuple, Optional

from narrators import NARRATOR_PROFILES, compute_mood_shift, describe_mood
from world_state import compute_world_state, compute_drift_signature, get_conditional_choices

_api_key: Optional[str] = os.environ.get("ANTHROPIC_API_KEY")
_client = None


def _get_client():
    global _client
    if _client is None and _api_key:
        import anthropic
        _client = anthropic.Anthropic(api_key=_api_key)
    return _client


# ---------------------------------------------------------------------------
# Story Graph
# Each node has:
#   "text"         — static fallback prose (used when no API key is set)
#   "scene_prompt" — fed to the LLM when an API key is available
#   "choices"      — choice text → next beat ID
# ---------------------------------------------------------------------------

STORY_GRAPH: Dict[str, dict] = {

    # --- Arc 1: The Doorway ---
    "intro": {
        "text": "A faint hum stirs the air. Before you, a doorway shimmers — light bending at its edges as if the world beyond is still deciding what to be.",
        "scene_prompt": "The player stands before a shimmering doorway in an unnamed, liminal place. The air hums with unresolved potential. Nothing has happened yet.",
        "choices": {
            "step through": "doorway_enter",
            "pull back": "doorway_hesitate",
            "speak to the light": "doorway_speak",
        },
        "arc": "the_doorway",
    },
    "doorway_enter": {
        "text": "You cross the threshold. The light folds around you like a living membrane, tasting your intent. The world behind you dissolves into soft static.",
        "scene_prompt": "The player crosses the threshold. The light folds around them like a living membrane, tasting their intent. The world behind them dissolves.",
        "choices": {
            "go deeper": "forest_edge",
            "look back": "doorway_regret",
            "call out": "forest_echo",
        },
        "arc": "the_doorway",
    },
    "doorway_hesitate": {
        "text": "You step back. The doorway dims — not in anger, but in quiet disappointment. The hum lowers to a slow, patient pulse. It will wait.",
        "scene_prompt": "The player steps back from the doorway. It dims slightly, as if disappointed. The hum lowers to a slow pulse. The choice remains open.",
        "choices": {
            "try again": "doorway_enter",
            "walk away": "path_alone",
            "wait and watch": "doorway_patience",
        },
        "arc": "the_doorway",
    },
    "doorway_speak": {
        "text": "You speak to the light directly. It stills — every ripple ceasing at once. Something vast and attentive turns toward you. The air thickens.",
        "scene_prompt": "The player addresses the light directly. It stills. Something vast and attentive listens. The air thickens with anticipation.",
        "choices": {
            "ask its name": "light_name",
            "ask where it leads": "light_destination",
            "fall silent": "light_silence",
        },
        "arc": "the_doorway",
    },
    "doorway_regret": {
        "text": "You look back. The world you came from is already dissolving — shapes losing their edges, colors bleeding into grey. There is no clean return.",
        "scene_prompt": "The player looks back through the threshold. The world they came from is already dissolving into soft static. There is no clean return.",
        "choices": {
            "go back anyway": "intro",
            "accept it and move forward": "forest_edge",
        },
        "arc": "the_doorway",
    },
    "doorway_patience": {
        "text": "You wait. Minutes pass, or perhaps hours — time moves strangely here. Slowly, the doorway brightens again. Patience, it seems, is its own kind of answer.",
        "scene_prompt": "The player waits. Minutes pass — or maybe hours. The doorway slowly brightens again, as if patience itself is a kind of answer.",
        "choices": {
            "step through now": "doorway_enter",
            "keep waiting": "doorway_wisdom",
        },
        "arc": "the_doorway",
    },
    "doorway_wisdom": {
        "text": "A long stillness. Then the light speaks first — one word, felt rather than heard: Ready. The doorway opens fully, wider than before, as if it finally trusts you.",
        "scene_prompt": "A long stillness. Then the light speaks first — one word, felt rather than heard: 'Ready.' The doorway opens fully, wider than before.",
        "choices": {
            "enter": "forest_edge",
            "bow and enter": "forest_edge",
        },
        "arc": "the_doorway",
    },

    # --- Arc 1: Light dialogue branch ---
    "light_name": {
        "text": "The light offers no name in words. Instead you feel a shape — something between a sound and a color pressed behind your eyes. It might be a name. It might be a warning.",
        "scene_prompt": "The light gives no name in words. Instead, the player feels a shape — something like a sound, something like a color. It might be a name. It might be a warning.",
        "choices": {
            "repeat the shape back": "doorway_enter",
            "let it go": "doorway_enter",
        },
        "arc": "the_doorway",
    },
    "light_destination": {
        "text": "The light flashes three images in quick succession: a forest edge draped in mist, a city of sealed gates, an open void where nothing presses back. Three paths. None guaranteed.",
        "scene_prompt": "The light shows a flash: a forest edge, a distant city, an open void. Three possibilities. None guaranteed.",
        "choices": {
            "step toward the forest flash": "forest_edge",
            "step toward the city flash": "city_gate",
            "step toward the void flash": "void_edge",
        },
        "arc": "the_doorway",
    },
    "light_silence": {
        "text": "You say nothing more. The light seems to appreciate this. It brightens slowly — not demanding, not rushing. An invitation without pressure.",
        "scene_prompt": "The player says nothing more. The light appreciates this. It brightens slowly, an invitation with no pressure attached.",
        "choices": {
            "walk through": "doorway_enter",
            "sit and wait": "doorway_patience",
        },
        "arc": "the_doorway",
    },

    # --- Arc 2: The Forest ---
    "forest_edge": {
        "text": "You stand at the edge of a forest that appears on no map. The trees are tall and remember things. Three paths diverge before you, each exhaling a different kind of dark.",
        "scene_prompt": "The player stands at the edge of a forest that has no name on any map. The trees are tall and remember things. Paths diverge in three directions.",
        "choices": {
            "follow the sound of water": "forest_stream",
            "climb the nearest tree": "forest_canopy",
            "press into the darkness": "forest_deep",
        },
        "arc": "the_forest",
    },
    "forest_echo": {
        "text": "You call out. Your voice travels strangely — returning seconds later from the wrong direction, slightly altered, as if the forest has an opinion about what you said.",
        "scene_prompt": "The player calls out. Their voice travels strangely — returning seconds later from the wrong direction, slightly altered.",
        "choices": {
            "listen to the altered echo": "forest_edge",
            "call out again": "forest_deep",
        },
        "arc": "the_forest",
    },
    "forest_stream": {
        "text": "You find a stream running uphill, quietly defying gravity. Something small and silver catches the light beneath the surface — moving with too much purpose to be natural.",
        "scene_prompt": "The player finds a stream running uphill, quietly defying gravity. Something small and silver moves in the current.",
        "choices": {
            "reach into the water": "forest_catch",
            "follow the stream upward": "forest_canopy",
            "drink from it": "forest_vision",
        },
        "arc": "the_forest",
    },
    "forest_canopy": {
        "text": "From the canopy you can see three things: the doorway you came from, still faintly glowing. A city of sealed towers in the distance. And a hole in the world where the void simply is.",
        "scene_prompt": "From the canopy the player can see: the doorway they came from, still faintly glowing. A city in the distance. And a hole in the world where the void is.",
        "choices": {
            "go toward the city": "city_gate",
            "go toward the void": "void_edge",
            "climb back down": "forest_edge",
        },
        "arc": "the_forest",
    },
    "forest_deep": {
        "text": "Deep in the forest, light fails entirely. Something ancient and utterly unconcerned moves nearby — immense, slow, breathing in geological time. It does not threaten. It simply exists.",
        "scene_prompt": "Deep in the forest, light fails. Something ancient and unconcerned moves nearby. It does not threaten — it simply exists, enormous and old.",
        "choices": {
            "approach it": "forest_ancient",
            "stay perfectly still": "forest_stillness",
            "back away slowly": "forest_edge",
        },
        "arc": "the_forest",
    },
    "forest_catch": {
        "text": "Your hand closes around something cold and impossible — a key, heavier than it looks, casting no reflection in the water. It fits no lock you know. Yet.",
        "scene_prompt": "The silver thing in the water is a key — cold, impossible, heavier than it looks. It fits no lock the player knows. Yet.",
        "choices": {
            "keep it": "city_gate",
            "put it back": "forest_stream",
        },
        "arc": "the_forest",
    },
    "forest_vision": {
        "text": "The water tastes like memory. You see a flash of somewhere else — a city square at dusk, a face you almost recognize, a door standing open in an empty room. Then it fades.",
        "scene_prompt": "The water tastes like memory. The player sees a flash of somewhere else — a city square, a face, a door. Then it fades.",
        "choices": {
            "try to hold the vision": "forest_stream",
            "let it go and move on": "forest_edge",
        },
        "arc": "the_forest",
    },
    "forest_ancient": {
        "text": "The ancient thing acknowledges you — not with words, but with a slow shift of presence. The way a mountain might notice a sparrow landing on its peak.",
        "scene_prompt": "The ancient thing acknowledges the player. Not with words. With a slow shift of presence — like a mountain noticing a sparrow.",
        "choices": {
            "ask it something": "forest_stillness",
            "leave it in peace": "forest_edge",
        },
        "arc": "the_forest",
    },
    "forest_stillness": {
        "text": "A long stillness. Then the ancient thing moves on, indifferent and enormous. The forest exhales. The air changes — something granted, though you cannot name what.",
        "scene_prompt": "Stillness. The ancient thing moves on. The forest exhales. The player is alone again, but the air feels different — permission given.",
        "choices": {
            "head toward the city": "city_gate",
            "head toward the void": "void_edge",
            "return to the forest edge": "forest_edge",
        },
        "conditional_choices": [
            {"condition": "ancient_met_and_doorway_mastered", "choice": "stay with it longer", "next_beat_id": "ancient_gift"},
        ],
        "arc": "the_forest",
    },

    # --- Arc 3: The Drift ---
    "city_gate": {
        "text": "The city gate is sealed. Above the arch, a single word is carved in a language you almost recognize — close enough to mean something, far enough to mean nothing. The doorway's hum is faint here, but present.",
        "scene_prompt": "The city gate is sealed. Above the arch: a single word in a language the player almost recognizes. The hum from the doorway is faint here, but present.",
        "choices": {
            "begin again from the start": "intro",
            "drift away": "drift_end",
        },
        "conditional_choices": [
            {"condition": "has_key", "choice": "use the key", "next_beat_id": "city_open"},
        ],
        "arc": "the_drift",
    },
    "void_edge": {
        "text": "At the edge of the void, there is no drama. Just an open quiet — the kind that waits without hunger. You can feel the shape of every choice that brought you here.",
        "scene_prompt": "At the edge of the void, there is no drama — just an open quiet. The player can feel the shape of every choice that led here.",
        "choices": {
            "step in": "drift_end",
            "turn back": "forest_edge",
        },
        "conditional_choices": [
            {"condition": "void_steps_gte_2", "choice": "step deeper", "next_beat_id": "void_depths"},
        ],
        "arc": "the_drift",
    },
    "path_alone": {
        "text": "You walk alone — no doorway, no forest, no city. Just a road that curves gently toward a horizon that keeps retreating. The hum is gone. The silence is yours.",
        "scene_prompt": "The player walks alone. No doorway, no forest, no city. Just a road that curves gently toward a horizon that keeps retreating.",
        "choices": {
            "keep walking": "drift_end",
            "stop and wait": "intro",
        },
        "arc": "the_drift",
    },
    "drift_end": {
        "text": "The drift ends. The hum goes quiet. A single point of light lingers — the seed of whatever comes next.",
        "scene_prompt": "The drift ends. The hum goes quiet. A single point of light remains — the seed of the next journey.",
        "choices": {
            "begin again": "intro",
        },
        "arc": "the_drift",
    },

    # --- State-gated nodes (require world state conditions) ---
    "city_open": {
        "text": "The key turns. The gate groans — not with resistance, but with recognition. The city beyond is not empty. It was waiting.",
        "scene_prompt": "The player uses a silver key found in an impossible stream to open the sealed city gate. The city was not abandoned — it was held in reserve.",
        "choices": {
            "step inside": "drift_end",
            "look back before entering": "city_open_pause",
        },
        "arc": "the_drift",
    },
    "city_open_pause": {
        "text": "You look back. The forest is still there — the doorway a faint smear of light between the trees. You could return. But the city breathes behind you, warm and patient.",
        "scene_prompt": "The player pauses at the open city gate, looking back at the forest and the distant doorway before deciding whether to enter.",
        "choices": {
            "enter the city": "drift_end",
            "go back to the forest": "forest_edge",
        },
        "arc": "the_drift",
    },
    "void_depths": {
        "text": "Deeper than before. The quiet here is older — the kind that predates sound. Something at the bottom of the void has noticed you've come back. It is not afraid.",
        "scene_prompt": "The player descends into the void for at least the second time. The void has begun to recognize them. Something stirs in its depths.",
        "choices": {
            "remain still": "drift_end",
            "reach toward what noticed you": "drift_end",
        },
        "arc": "the_drift",
    },
    "ancient_gift": {
        "text": "The ancient thing shifts. Something releases from it — not given, exactly. Transferred. You carry it now without knowing what it is. The forest exhales around you both.",
        "scene_prompt": "The ancient thing in the forest recognizes the player has both faced it before and learned patience at the doorway. It offers something wordless — a transfer of presence.",
        "choices": {
            "accept it": "drift_end",
            "leave it where it is": "forest_edge",
        },
        "arc": "the_forest",
    },
}


# ---------------------------------------------------------------------------
# Choice resolution
# ---------------------------------------------------------------------------

def resolve_choice(node: dict, player_choice: str) -> str:
    """Maps player_choice text to next beat ID. Falls back gracefully."""
    choices = node.get("choices", {})
    normalized = player_choice.lower().strip()

    if normalized in choices:
        return choices[normalized]

    for key, target in choices.items():
        if key in normalized or normalized in key:
            return target

    if choices:
        return next(iter(choices.values()))

    return "intro"


# ---------------------------------------------------------------------------
# History summary
# ---------------------------------------------------------------------------

def summarize_history(history: list) -> str:
    if not history:
        return "No prior choices."
    recent = history[-3:]
    parts = [f"chose '{h.get('player_choice', '?')}'" for h in recent]
    return "Player recently " + ", then ".join(parts) + "."


# ---------------------------------------------------------------------------
# Narrator memory extraction
# ---------------------------------------------------------------------------

LANDMARK_BEATS = {
    "forest_catch":    "found a silver key in an uphill stream",
    "forest_ancient":  "stood before the ancient thing in the deep forest",
    "forest_vision":   "drank from the impossible stream and saw visions",
    "doorway_wisdom":  "waited in silence until the light spoke first",
    "void_edge":       "stood at the edge of the void",
    "doorway_hesitate":"hesitated at the threshold",
    "drift_end":       "completed a full drift",
}


def extract_narrator_memory(history: list, session_count: int = 1) -> str:
    if not history and session_count <= 1:
        return ""
    visited = {h.get("beat_id") for h in history}
    landmarks = [desc for beat_id, desc in LANDMARK_BEATS.items() if beat_id in visited]
    parts = []
    if session_count > 1:
        parts.append(f"This is the player's {session_count}{'rd' if session_count == 3 else 'th' if session_count > 3 else 'nd'} drift.")
    if landmarks:
        parts.append("They previously: " + ", ".join(landmarks) + ".")
    if parts:
        parts.append("The narrator remembers.")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Context-aware static text (used when no API key is set)
# ---------------------------------------------------------------------------

_NARRATOR_SUFFIXES = {
    "The Whisperer": " The air shivers with unspoken meaning.",
    "The Warden":    "",
    "The Trickster": " You sense laughter somewhere behind your thoughts.",
    "The Oracle":    " The shape of what comes next trembles at the edge of knowing.",
    "The Exile":     " It feels like a place you have lost before.",
}

_STATIC_VARIANTS = {
    "intro": [
        (lambda visited, count: count > 1,
         "The hum is familiar now."),
    ],
    "city_gate": [
        (lambda visited, count: "forest_catch" in visited,
         "The key in your pocket grows heavier as you approach."),
    ],
    "void_edge": [
        (lambda visited, count: "void_edge" in visited,
         "You know this quiet. You've stood here before."),
    ],
    "drift_end": [
        (lambda visited, count: count > 1,
         "Again, the drift ends. It gets easier to let go."),
    ],
}


def get_static_beat(node: dict, beat_id: str, history: list, narrator: str, session_count: int = 1) -> str:
    base_text = node["text"]
    visited = {h.get("beat_id") for h in history}
    variants = _STATIC_VARIANTS.get(beat_id, [])
    for condition, prefix in variants:
        if condition(visited, session_count):
            base_text = prefix + " " + base_text
            break
    suffix = _NARRATOR_SUFFIXES.get(narrator, "")
    return base_text + suffix


# ---------------------------------------------------------------------------
# LLM beat generation
# ---------------------------------------------------------------------------

def generate_beat_with_llm(
    scene_prompt: str,
    static_text: str,
    beat_id: str,
    narrator_profile: dict,
    history_summary: str,
    player_choice: str,
    mood: dict,
    history: list,
    session_count: int,
    drift_signature: str = "The Drifter",
) -> str:
    client = _get_client()

    if client is None:
        return get_static_beat(
            node={"text": static_text},
            beat_id=beat_id,
            history=history,
            narrator=narrator_profile["name"],
            session_count=session_count,
        )

    mood_desc = describe_mood(mood)
    narrator_memory = extract_narrator_memory(history, session_count)

    system_parts = [
        f"You are {narrator_profile['name']}, a narrator in an interactive micro-adventure story.",
        f"Tone: {narrator_profile['tone']}",
        f"Behavior: {narrator_profile['behavior']}",
        f"Your current emotional state toward the player: {mood_desc}",
        f"Drift Signature: {drift_signature}",
    ]
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
        max_tokens=300,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text.strip()


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def generate_next_beat(
    history: List[Dict],
    player_choice: str,
    narrator: str,
    current_beat_id: str = "intro",
    session_count: int = 1,
) -> Tuple[str, List[str], str, Dict, str]:
    """
    Returns (beat_text, choices_list, next_beat_id, mood, drift_signature).
    Uses LLM-generated prose when ANTHROPIC_API_KEY is set; static text otherwise.
    Conditional choices are resolved and displayed seamlessly based on world state.
    """
    node = STORY_GRAPH.get(current_beat_id, STORY_GRAPH["intro"])
    mood = compute_mood_shift(history)
    world_state = compute_world_state(history, session_count)
    drift_signature = compute_drift_signature(world_state, mood)

    # Resolve player choice against base + conditional choices for this node
    extra_current = get_conditional_choices(node, world_state)
    extended_current = {**node["choices"], **{c: t for c, t in extra_current}}
    augmented_node = {**node, "choices": extended_current}
    next_beat_id = resolve_choice(augmented_node, player_choice)

    next_node = STORY_GRAPH.get(next_beat_id, STORY_GRAPH["intro"])

    # Build display choices for next node, including its conditional unlocks
    extra_next = get_conditional_choices(next_node, world_state)
    display_choices = list(next_node["choices"].keys()) + [c for c, _ in extra_next]

    narrator_profile = NARRATOR_PROFILES.get(narrator, NARRATOR_PROFILES["The Whisperer"])
    history_summary = summarize_history(history)

    beat_text = generate_beat_with_llm(
        scene_prompt=next_node["scene_prompt"],
        static_text=next_node["text"],
        beat_id=next_beat_id,
        narrator_profile=narrator_profile,
        history_summary=history_summary,
        player_choice=player_choice,
        mood=mood,
        history=history,
        session_count=session_count,
        drift_signature=drift_signature,
    )

    return beat_text, display_choices, next_beat_id, mood, drift_signature
