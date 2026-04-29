import random
from typing import Dict, List, Optional, Tuple

from adventures.last_voicemail import ADVENTURE_META as _VM_META, STORY_GRAPH as _VM_GRAPH, LANDMARK_BEATS as _VM_LANDMARKS
from adventures.the_cartographer import ADVENTURE_META as _CART_META, STORY_GRAPH as _CART_GRAPH, LANDMARK_BEATS as _CART_LANDMARKS
from adventures.crew_of_the_meridian import ADVENTURE_META as _MER_META, STORY_GRAPH as _MER_GRAPH, LANDMARK_BEATS as _MER_LANDMARKS
from adventures.open_premises import OPEN_PREMISES

_GUIDED_ADVENTURES = {
    "last_voicemail": {
        "meta": _VM_META,
        "graph": _VM_GRAPH,
        "landmarks": _VM_LANDMARKS,
    },
    "the_cartographer": {
        "meta": _CART_META,
        "graph": _CART_GRAPH,
        "landmarks": _CART_LANDMARKS,
    },
    "crew_of_the_meridian": {
        "meta": _MER_META,
        "graph": _MER_GRAPH,
        "landmarks": _MER_LANDMARKS,
    },
}

_OPEN_PREMISES_MAP = {p["id"]: p for p in OPEN_PREMISES}


def get_adventure(adventure_id: str) -> Optional[dict]:
    return _GUIDED_ADVENTURES.get(adventure_id)


def list_adventures() -> List[dict]:
    return sorted(
        [adv["meta"] for adv in _GUIDED_ADVENTURES.values()],
        key=lambda m: m["estimated_minutes"],
    )


def get_open_premises() -> List[dict]:
    return OPEN_PREMISES


def get_premise(premise_id: str) -> Optional[dict]:
    return _OPEN_PREMISES_MAP.get(premise_id)


def resolve_choice(node: dict, player_choice: str) -> Tuple[str, bool]:
    """
    Returns (next_beat_id, rng_triggered).
    Supports both legacy string values and new RNG dict format.
    """
    choices = node.get("choices", {})
    normalized = player_choice.lower().strip()

    # Find the matching key
    matched_key = None
    if normalized in choices:
        matched_key = normalized
    else:
        for key in choices:
            if key in normalized or normalized in key:
                matched_key = key
                break
    if matched_key is None and choices:
        matched_key = next(iter(choices))

    if matched_key is None:
        return "intro", False

    value = choices[matched_key]

    # Legacy string format
    if isinstance(value, str):
        return value, False

    # Fixed format
    if isinstance(value, dict) and value.get("type") == "fixed":
        return value["next_beat_id"], False

    # RNG format
    if isinstance(value, dict) and value.get("type") == "rng":
        outcomes = value["outcomes"]
        total = sum(o["weight"] for o in outcomes)
        roll = random.randint(1, total)
        cumulative = 0
        for outcome in outcomes:
            cumulative += outcome["weight"]
            if roll <= cumulative:
                return outcome["next_beat_id"], True
        return outcomes[-1]["next_beat_id"], True

    return "intro", False
