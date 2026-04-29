import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_SESSIONS_DIR = Path(__file__).parent / "sessions"


def _path(session_id: str) -> Path:
    return _SESSIONS_DIR / f"{session_id}.json"


def create_session(narrator: str) -> dict:
    _SESSIONS_DIR.mkdir(exist_ok=True)
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    data = {
        "session_id": session_id,
        "narrator": narrator,
        "history": [],
        "current_beat_id": "intro",
        "session_count": 1,
        "world_state": {},
        "drift_signature": "The Drifter",
        "created_at": now,
        "last_played": now,
    }
    _path(session_id).write_text(json.dumps(data, indent=2))
    return data


def load_session(session_id: str) -> Optional[dict]:
    p = _path(session_id)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def save_session(session_id: str, updates: dict) -> None:
    p = _path(session_id)
    if not p.exists():
        return
    data = json.loads(p.read_text())
    data.update(updates)
    data["last_played"] = datetime.now(timezone.utc).isoformat()
    p.write_text(json.dumps(data, indent=2))


def list_sessions() -> list:
    if not _SESSIONS_DIR.exists():
        return []
    sessions = []
    for p in _SESSIONS_DIR.glob("*.json"):
        try:
            data = json.loads(p.read_text())
            sessions.append({
                "session_id": data["session_id"],
                "narrator": data.get("narrator", ""),
                "drift_signature": data.get("drift_signature", "The Drifter"),
                "arc": data.get("current_beat_id", "intro"),
                "session_count": data.get("session_count", 1),
                "last_played": data.get("last_played", ""),
                "created_at": data.get("created_at", ""),
            })
        except Exception:
            pass
    return sorted(sessions, key=lambda s: s["last_played"], reverse=True)


def increment_session_count(session_id: str) -> int:
    """Call when player reaches drift_end and begins again. Returns new count."""
    p = _path(session_id)
    if not p.exists():
        return 1
    data = json.loads(p.read_text())
    data["session_count"] = data.get("session_count", 1) + 1
    data["last_played"] = datetime.now(timezone.utc).isoformat()
    p.write_text(json.dumps(data, indent=2))
    return data["session_count"]
