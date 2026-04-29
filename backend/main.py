import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

from story_engine import generate_next_beat, STORY_GRAPH
from narrators import NARRATOR_PROFILES, compute_mood_shift
from world_state import compute_world_state, compute_drift_signature
from session_store import create_session, load_session, save_session, increment_session_count, list_sessions

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Mythdrift Backend", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request / Response Models
# -----------------------------

class HistoryItem(BaseModel):
    player_choice: str
    beat_id: str
    narrator_beat: str


class MythdriftRequest(BaseModel):
    history: List[HistoryItem]
    player_choice: str
    narrator: str
    current_beat_id: str = "intro"
    session_id: Optional[str] = None


class MythdriftResponse(BaseModel):
    next_beat: str
    choices: List[str]
    next_beat_id: str
    mood: Dict[str, float]
    drift_signature: str


class CreateSessionRequest(BaseModel):
    narrator: str


# -----------------------------
# Endpoints
# -----------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/narrators")
def get_narrators():
    return {
        "narrators": [
            {"name": name, "tone": data["tone"], "behavior": data["behavior"]}
            for name, data in NARRATOR_PROFILES.items()
        ]
    }


@app.get("/sessions")
def list_sessions_endpoint():
    return {"sessions": list_sessions()}


@app.post("/session")
def create_session_endpoint(body: CreateSessionRequest):
    session = create_session(body.narrator)
    return {
        "session_id": session["session_id"],
        "session_count": session["session_count"],
        "drift_signature": session["drift_signature"],
    }


@app.get("/session/{session_id}")
def get_session_endpoint(session_id: str):
    session = load_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    beat_id = session.get("current_beat_id", "intro")
    arc = STORY_GRAPH.get(beat_id, {}).get("arc", "the_doorway")
    history = session.get("history", [])
    session_count = session.get("session_count", 1)
    mood = compute_mood_shift(history)
    world_state = compute_world_state(history, session_count)
    drift_signature = session.get("drift_signature") or compute_drift_signature(world_state, mood)
    return {**session, "arc": arc, "mood": mood, "drift_signature": drift_signature}


@app.post("/mythdrift", response_model=MythdriftResponse)
def mythdrift_endpoint(request: MythdriftRequest):
    history_dicts = [item.model_dump() for item in request.history]

    session_count = 1
    if request.session_id:
        session = load_session(request.session_id)
        if session:
            session_count = session.get("session_count", 1)

    next_beat, choices, next_beat_id, mood, drift_signature = generate_next_beat(
        history=history_dicts,
        player_choice=request.player_choice,
        narrator=request.narrator,
        current_beat_id=request.current_beat_id,
        session_count=session_count,
    )

    if request.session_id:
        updated_history = history_dicts + [{
            "player_choice": request.player_choice,
            "beat_id": next_beat_id,
            "narrator_beat": next_beat,
        }]
        world_state = compute_world_state(updated_history, session_count)
        updates = {
            "history": updated_history,
            "current_beat_id": next_beat_id,
            "world_state": world_state,
            "drift_signature": drift_signature,
        }
        if next_beat_id == "drift_end":
            new_count = increment_session_count(request.session_id)
            updates["session_count"] = new_count
        else:
            save_session(request.session_id, updates)

    return MythdriftResponse(
        next_beat=next_beat,
        choices=choices,
        next_beat_id=next_beat_id,
        mood=mood,
        drift_signature=drift_signature,
    )
