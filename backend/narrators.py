from typing import Dict

NARRATOR_PROFILES: Dict[str, dict] = {
    "The Whisperer": {
        "name": "The Whisperer",
        "tone": "soft, cryptic, dreamlike",
        "behavior": "guides the player gently but never directly",
        "style": {
            "metaphor_level": 0.7,
            "sentence_length": "medium",
            "emotion_bias": "mysterious"
        },
        "mood_weights": {
            "trust": ["wait", "listen", "observe", "stay", "speak softly"],
            "suspicion": ["demand", "defy", "ignore", "resist", "refuse"],
            "curiosity": ["ask", "explore", "reach", "touch", "examine"]
        }
    },

    "The Warden": {
        "name": "The Warden",
        "tone": "stern, commanding, precise",
        "behavior": "pushes the player toward decisive action",
        "style": {
            "metaphor_level": 0.2,
            "sentence_length": "short",
            "emotion_bias": "strict"
        },
        "mood_weights": {
            "trust": ["comply", "accept", "follow", "stand firm", "obey"],
            "suspicion": ["hesitate", "waver", "retreat", "pull back", "turn away"],
            "curiosity": ["assess", "evaluate", "approach", "investigate", "scan"]
        }
    },

    "The Trickster": {
        "name": "The Trickster",
        "tone": "playful, chaotic, teasing",
        "behavior": "mocks the player and bends the rules",
        "style": {
            "metaphor_level": 0.9,
            "sentence_length": "varied",
            "emotion_bias": "unpredictable"
        },
        "mood_weights": {
            "trust": ["play along", "laugh", "embrace", "let go", "accept it"],
            "suspicion": ["resist", "argue", "call out", "reject", "mock back"],
            "curiosity": ["reach", "poke", "try", "experiment", "break it"]
        }
    },

    "The Oracle": {
        "name": "The Oracle",
        "tone": "prophetic, detached, speaking in riddles",
        "behavior": "reveals fragments of futures the player hasn't earned yet",
        "style": {
            "metaphor_level": 0.8,
            "sentence_length": "varied",
            "emotion_bias": "revelatory"
        },
        "mood_weights": {
            "trust": ["accept", "believe", "follow the sign", "heed", "listen"],
            "suspicion": ["doubt", "question", "challenge", "demand proof", "deny"],
            "curiosity": ["seek", "unravel", "decipher", "ask", "interpret"]
        }
    },

    "The Exile": {
        "name": "The Exile",
        "tone": "bitter, nostalgic, world-weary",
        "behavior": "mourns what was lost and judges the player's choices harshly",
        "style": {
            "metaphor_level": 0.6,
            "sentence_length": "long",
            "emotion_bias": "melancholic"
        },
        "mood_weights": {
            "trust": ["remember", "honor", "stay", "preserve", "cherish"],
            "suspicion": ["abandon", "forget", "destroy", "ignore", "discard"],
            "curiosity": ["search", "find", "uncover", "return", "recall"]
        }
    }
}


def compute_mood_shift(history: list) -> Dict[str, float]:
    """Analyzes player choices to produce a mood state dict (0.0–1.0 per axis)."""
    trust = 0.0
    suspicion = 0.0
    curiosity = 0.0

    if not history:
        return {"trust": trust, "suspicion": suspicion, "curiosity": curiosity}

    for item in history:
        choice = item.get("player_choice", "").lower()
        trust_words = ["wait", "listen", "accept", "stay", "comply", "follow",
                       "honor", "remember", "play along", "believe", "heed"]
        suspicion_words = ["demand", "defy", "resist", "refuse", "ignore", "retreat",
                           "doubt", "question", "deny", "abandon", "reject"]
        curiosity_words = ["explore", "reach", "touch", "ask", "seek", "examine",
                           "investigate", "unravel", "search", "find", "try"]

        for word in trust_words:
            if word in choice:
                trust += 1.0
        for word in suspicion_words:
            if word in choice:
                suspicion += 1.0
        for word in curiosity_words:
            if word in choice:
                curiosity += 1.0

    total = max(len(history), 1)
    return {
        "trust": min(trust / total, 1.0),
        "suspicion": min(suspicion / total, 1.0),
        "curiosity": min(curiosity / total, 1.0),
    }


def describe_mood(mood: Dict[str, float]) -> str:
    """Converts mood floats into a natural-language phrase for the LLM prompt."""
    parts = []
    if mood["trust"] > 0.4:
        parts.append("growing trust toward the player")
    if mood["suspicion"] > 0.4:
        parts.append("rising suspicion of the player's motives")
    if mood["curiosity"] > 0.4:
        parts.append("keen curiosity about the player's path")
    if not parts:
        return "neutral — no strong emotional lean yet"
    return ", ".join(parts)
