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
        },
        "flavor_lines": {
            "dread":     "Something here already knows how this ends.",
            "wonder":    "There are places that remember being looked at.",
            "defiance":  "The world has noted your resistance. It is patient.",
            "discovery": "Most people walk past this. You stopped.",
            "loss":      "What remains is always the part that mattered.",
            "threshold": "The door only looks like a door from this side.",
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
        },
        "flavor_lines": {
            "dread":     "Identify the threat. Address it.",
            "wonder":    "Note it. Move on. Wonder later.",
            "defiance":  "Good. That instinct will serve you.",
            "discovery": "File it. What's next.",
            "loss":      "Absorb it. Keep moving.",
            "threshold": "Decision point. Choose.",
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
        },
        "flavor_lines": {
            "dread":     "Oh, that face. That's the face people make right before it gets interesting.",
            "wonder":    "See? And you almost didn't come.",
            "defiance":  "There it is. That's the version of you I was waiting for.",
            "discovery": "You found the thing. Don't celebrate yet. You still have to do something about it.",
            "loss":      "Well. That happened.",
            "threshold": "Go on then. I'll be right here, judging.",
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
        },
        "flavor_lines": {
            "dread":     "This moment was always going to happen.",
            "wonder":    "The shape of what comes next is already in the room.",
            "defiance":  "Resistance is one of the paths. It leads somewhere.",
            "discovery": "You have found what you were always going to find.",
            "loss":      "Loss is a form of arrival.",
            "threshold": "What is on the other side has been waiting your entire life.",
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
        },
        "flavor_lines": {
            "dread":     "I know this feeling. I lived in it for years.",
            "wonder":    "I used to feel that. Before.",
            "defiance":  "Careful. That worked once. Then it didn't.",
            "discovery": "And now you know. That's the part no one warns you about.",
            "loss":      "Yes. That's what it costs. Every time.",
            "threshold": "I stood where you're standing. I chose wrong. You might do better.",
        }
    }
}


def compute_mood_shift(history: list) -> Dict[str, float]:
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
                           "investigate", "unravel", "search", "find", "try",
                           "read", "check", "look", "open", "go to"]

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
