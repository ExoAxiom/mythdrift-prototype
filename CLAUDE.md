# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Mythdrift is a voice-driven micro-adventure engine. A FastAPI backend generates story beats using a branching story graph; a Flutter client handles voice I/O, narrator selection, and renders the story loop. The two communicate over HTTP.

## Commands

### Backend
```powershell
# Install dependencies (run once, from backend/)
pip install -r requirements.txt

# Start the development server
cd E:\mythdrift_prototype\backend
python -m uvicorn main:app --reload --port 5000
```

Backend runs at `http://localhost:5000`. Swagger UI at `http://localhost:5000/docs`.

### Flutter
```powershell
# Install packages (run once)
flutter pub get

# Run on Chrome (recommended on Windows — flutter_tts fails to compile on Windows desktop due to missing NuGet)
flutter run -d chrome

# List available devices
flutter devices
```

**Platform note:** `flutter_tts` requires NuGet to build on Windows desktop — it will fail with a CMake error. Use Chrome (`-d chrome`) or an Android emulator instead.

## Architecture

### Two independent processes

```
Flutter client  ──HTTP──►  FastAPI backend  ──(optional)──►  Anthropic API
lib/                        backend/
```

The Flutter app holds all session state in memory. The backend is stateless — every request includes the full history array.

### Backend (`backend/`)

**`main.py`** — FastAPI app. Three endpoints:
- `GET /health`
- `GET /narrators` — returns all narrator profiles (name, tone, behavior)
- `POST /mythdrift` — main story endpoint; takes `{history, player_choice, narrator, current_beat_id}`, returns `{next_beat, choices, next_beat_id}`

**`story_engine.py`** — The core. Two modes:
- **Static mode** (no `ANTHROPIC_API_KEY`): returns pre-written prose from `STORY_GRAPH[node]["text"]` with a narrator-specific suffix appended
- **LLM mode** (key present): calls `claude-haiku-4-5-20251001` with the node's `"scene_prompt"` and narrator persona as system prompt

`resolve_choice()` does fuzzy matching so voice input doesn't need to be exact. Falls back to the first valid choice if nothing matches.

**`narrators.py`** — Five narrator profiles (Whisperer, Warden, Trickster, Oracle, Exile). `compute_mood_shift(history)` scores trust/suspicion/curiosity from accumulated choices. `describe_mood()` converts scores to a natural-language phrase injected into the LLM system prompt.

### Flutter (`lib/`)

**`main.dart`** → **`screens/narrator_selection_screen.dart`** → **`prototype_screen.dart`**

`NarratorSelectionScreen` fetches `/narrators` on init and displays narrator cards. Tapping one pushes `PrototypeScreen(narrator: name)`.

`PrototypeScreen` owns all session state: `_storyHistory` (list of `{player_choice, beat_id, narrator_beat}`), `_currentBeatId`, `_choices`, `_isLoading`. Choices render as `OutlinedButton` widgets. The mic button triggers `speech_to_text`; recognized speech is sent directly to `_sendChoiceToBackend()`. TTS speaks every incoming beat via `flutter_tts`.

**`services/mythdrift_api.dart`** — Static HTTP client. `_baseUrl` must match the environment:
- Chrome / iOS simulator: `http://localhost:5000`
- Android emulator: `http://10.0.2.2:5000`
- Physical device: your machine's LAN IP

### Story Graph

Defined entirely in `backend/story_engine.py` as `STORY_GRAPH` — a dict of beat nodes. Each node has `"text"` (static prose), `"scene_prompt"` (LLM context), `"choices"` (choice text → next beat ID), and `"arc"`. Currently ~20 nodes across three arcs: *The Doorway*, *The Forest*, *The Drift*. `drift_end` loops back to `intro`.

### LLM integration

The Anthropic client is lazy-loaded only when `ANTHROPIC_API_KEY` is set. Without it the backend runs fully offline. To enable LLM narration, create `backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
```
`python-dotenv` loads this automatically on startup.

## PowerShell note

This project is developed on Windows. Use `;` to chain commands, not `&&`:
```powershell
cd backend; python -m uvicorn main:app --reload --port 5000
```
