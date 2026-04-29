from typing import Dict, List, Tuple

_CONDITIONS = {
    "has_key":                          lambda ws: ws["has_key"],
    "void_steps_gte_2":                 lambda ws: ws["void_steps"] >= 2,
    "ancient_met_and_doorway_mastered": lambda ws: ws["ancient_met"] and ws["doorway_mastered"],
}


def compute_world_state(history: list, session_count: int = 1) -> Dict:
    visited = {h.get("beat_id") for h in history}
    void_steps = sum(1 for h in history if h.get("beat_id") == "void_edge")
    return {
        "has_key":          "forest_catch"   in visited,
        "ancient_met":      "forest_ancient" in visited,
        "doorway_mastered": "doorway_wisdom" in visited,
        "visions_seen":     "forest_vision"  in visited,
        "city_reached":     "city_gate"      in visited,
        "void_steps":       void_steps,
        "drifts_completed": session_count,
    }


def compute_drift_signature(world_state: Dict, mood: Dict) -> str:
    ws = world_state
    if ws["void_steps"] >= 2:
        return "The Void-Walker"
    if ws["doorway_mastered"]:
        return "The Patient"
    if ws["has_key"] and ws["ancient_met"]:
        return "The Seeker"
    if ws["visions_seen"] and ws["drifts_completed"] >= 2:
        return "The Wanderer"
    if ws["drifts_completed"] >= 3 and mood.get("trust", 0) > 0.3:
        return "The Resolute"
    if mood.get("suspicion", 0) > 0.4:
        return "The Hesitant"
    return "The Drifter"


def get_conditional_choices(node: dict, world_state: Dict) -> List[Tuple[str, str]]:
    """Returns list of (choice_text, next_beat_id) tuples for unlocked conditional choices."""
    result = []
    for cc in node.get("conditional_choices", []):
        cond_fn = _CONDITIONS.get(cc["condition"])
        if cond_fn and cond_fn(world_state):
            result.append((cc["choice"], cc["next_beat_id"]))
    return result
