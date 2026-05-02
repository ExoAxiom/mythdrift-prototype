import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Dict, Optional

from story_engine import generate_next_beat
from narrators import NARRATOR_PROFILES, compute_mood_shift
from world_state import compute_world_state, compute_drift_signature
from session_store import create_session, load_session, save_session, increment_session_count, list_sessions
from adventure_registry import list_adventures, get_open_premises

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Mythdrift Backend", version="0.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str, request: Request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Private-Network": "true",
    }
    return Response(status_code=204, headers=headers)


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
    adventure_id: str = "last_voicemail"
    adventure_type: str = "guided"


class MythdriftResponse(BaseModel):
    next_beat: str
    choices: List[str]
    next_beat_id: str
    mood: Dict[str, float]
    drift_signature: str
    rng_triggered: bool


class CreateSessionRequest(BaseModel):
    narrator: str
    adventure_id: str = "last_voicemail"
    adventure_type: str = "guided"


# -----------------------------
# Endpoints
# -----------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "gemini_key_set": bool(os.environ.get("GEMINI_API_KEY")),
        "anthropic_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }


@app.get("/narrators")
def get_narrators():
    return {
        "narrators": [
            {"name": name, "tone": data["tone"], "behavior": data["behavior"]}
            for name, data in NARRATOR_PROFILES.items()
        ]
    }


@app.get("/adventures")
def get_adventures():
    return {"adventures": list_adventures()}


@app.get("/adventures/open-premises")
def get_premises():
    return {"premises": get_open_premises()}


@app.get("/sessions")
def list_sessions_endpoint():
    return {"sessions": list_sessions()}


@app.post("/session")
def create_session_endpoint(body: CreateSessionRequest):
    session = create_session(body.narrator, body.adventure_id, body.adventure_type)
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
    history = session.get("history", [])
    session_count = session.get("session_count", 1)
    mood = compute_mood_shift(history)
    world_state = compute_world_state(history, session_count)
    drift_signature = session.get("drift_signature") or compute_drift_signature(world_state, mood)

    from adventure_registry import get_adventure
    adventure_id = session.get("adventure_id", "last_voicemail")
    adventure = get_adventure(adventure_id)
    arc = "guided"
    if adventure:
        node = adventure["graph"].get(beat_id, {})
        arc = node.get("arc", "guided")

    return {**session, "arc": arc, "mood": mood, "drift_signature": drift_signature}


@app.post("/mythdrift", response_model=MythdriftResponse)
def mythdrift_endpoint(request: MythdriftRequest):
    history_dicts = [item.model_dump() for item in request.history]

    session_count = 1
    if request.session_id:
        session = load_session(request.session_id)
        if session:
            session_count = session.get("session_count", 1)

    next_beat, choices, next_beat_id, mood, drift_signature, rng_triggered = generate_next_beat(
        history=history_dicts,
        player_choice=request.player_choice,
        narrator=request.narrator,
        current_beat_id=request.current_beat_id,
        session_count=session_count,
        adventure_id=request.adventure_id,
        adventure_type=request.adventure_type,
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
            "adventure_id": request.adventure_id,
            "adventure_type": request.adventure_type,
        }
        is_end = next_beat_id in ("end_safe", "end_loop", "end_static", "end_free",
                                  "end_mapped", "end_forgotten", "end_broadcast",
                                  "end_remains", "end_silence", "end_waiting")
        if is_end:
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
        rng_triggered=rng_triggered,
    )
