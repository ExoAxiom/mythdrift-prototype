ADVENTURE_META = {
    "id": "last_voicemail",
    "title": "Last Voicemail",
    "genre": "Horror",
    "description": "A voicemail from an unknown number. The voice is yours. It's warning you about tonight.",
    "estimated_minutes": 5,
    "type": "guided",
    "tags": ["horror", "short", "solo", "suspense"],
}

LANDMARK_BEATS = {
    "vm_connects":  "heard their own voice warn them from the other end",
    "vm_static":    "heard breathing where there should have been silence",
    "vm_loop":      "became part of the loop",
    "vm_check_door":"looked through the peephole",
    "end_safe":     "survived the night",
    "end_loop":     "became the voice in the voicemail",
    "end_static":   "dissolved into static",
}

STORY_GRAPH = {

    "intro": {
        "text": (
            "Your phone buzzes on the nightstand. 11:04 PM. New voicemail, unknown number. "
            "You almost ignore it. Then you hear the first three words and your hand goes still. "
            "The voice is yours. It says: don't answer the door tonight."
        ),
        "scene_prompt": (
            "The player has just discovered a voicemail on their phone from an unknown number. "
            "The voice in the recording is their own. It warns them not to answer the door tonight. "
            "They have not yet decided what to do."
        ),
        "tone": "dread",
        "choices": {
            "check who called": "vm_check_number",
            "call the number back": {
                "type": "rng",
                "outcomes": [
                    {"weight": 50, "next_beat_id": "vm_connects"},
                    {"weight": 35, "next_beat_id": "vm_static"},
                    {"weight": 15, "next_beat_id": "vm_loop"},
                ]
            },
            "delete it and try to sleep": "vm_ignore",
        },
        "arc": "discovery",
    },

    "vm_check_number": {
        "text": (
            "The number is eleven digits. No carrier format you recognize. "
            "You search it — not 'no results,' just nothing, "
            "like the query dissolves before it reaches anything. "
            "Your own call history shows no outgoing calls to it. But the voicemail is there."
        ),
        "scene_prompt": (
            "The player is investigating the phone number from the voicemail. "
            "It has eleven digits and returns no search results. "
            "Their own call history shows nothing. The voicemail still exists."
        ),
        "tone": "discovery",
        "choices": {
            "call it back": {
                "type": "rng",
                "outcomes": [
                    {"weight": 50, "next_beat_id": "vm_connects"},
                    {"weight": 35, "next_beat_id": "vm_static"},
                    {"weight": 15, "next_beat_id": "vm_loop"},
                ]
            },
            "screenshot it and wait": "vm_clock",
        },
        "arc": "discovery",
    },

    "vm_connects": {
        "text": (
            "One ring. Then your voice answers — not a recording, "
            "you can hear yourself breathing, thinking. "
            "'You found it,' it says. 'Good. The door. Don't answer it. "
            "It's been standing outside since nine. It looks like someone you know.'"
        ),
        "scene_prompt": (
            "The player called back the unknown number and their own voice answered. "
            "It tells them something has been standing outside their door since 9 PM. "
            "It looks like someone familiar."
        ),
        "tone": "dread",
        "choices": {
            "ask who it looks like": "vm_asks_who",
            "hang up and check the door": "vm_check_door",
            "ask yourself what you know": "vm_asks_self",
        },
        "arc": "confrontation",
    },

    "vm_asks_who": {
        "text": (
            "You ask. There's a pause — the kind that means the answer is being chosen carefully. "
            "'It looks like whoever you'd open the door for,' your voice says. "
            "'That's the point. That's always been the point.' Then the line goes dead."
        ),
        "scene_prompt": (
            "The player asked who is outside. Their own voice on the phone said "
            "it looks like whoever they would open the door for — then hung up."
        ),
        "tone": "dread",
        "choices": {
            "check the door anyway": "vm_check_door",
            "barricade it and wait for morning": "vm_clock",
        },
        "arc": "confrontation",
    },

    "vm_asks_self": {
        "text": (
            "A long silence. Then: 'You already know. You called yourself, didn't you? "
            "At some point tonight, you will make this call. You will say these words. "
            "Something will happen between now and then.' The line goes cold."
        ),
        "scene_prompt": (
            "The player asked their future self what they know. "
            "The voice implied they will make this call themselves later tonight — "
            "that the loop has already begun."
        ),
        "tone": "threshold",
        "choices": {
            "check the door": "vm_check_door",
            "try to escape through another exit": "vm_clock",
        },
        "arc": "confrontation",
    },

    "vm_static": {
        "text": (
            "It rings twice. Then static — but underneath it, breathing. "
            "Slow. Patient. Not afraid of silence the way humans are. "
            "You listen for forty seconds before you hang up, and the breathing never changes pace."
        ),
        "scene_prompt": (
            "The player called the number and got static with slow, patient breathing underneath it. "
            "It continued unchanged for forty seconds before they hung up."
        ),
        "tone": "dread",
        "choices": {
            "check the door": "vm_check_door",
            "play the original voicemail again": "vm_replay",
            "sit in silence and listen to the apartment": "vm_clock",
        },
        "arc": "confrontation",
    },

    "vm_replay": {
        "text": (
            "You play it again. This time there are four more words at the end — "
            "words that weren't there before. "
            "Your voice says: *it can hear the phone.* "
            "You realize you've been listening with the speaker on."
        ),
        "scene_prompt": (
            "The player replayed the voicemail and discovered four new words at the end: "
            "'it can hear the phone.' The speaker has been on the whole time."
        ),
        "tone": "dread",
        "choices": {
            "immediately silence the phone": "vm_clock",
            "drop the phone and check the door": "vm_check_door",
        },
        "arc": "confrontation",
    },

    "vm_loop": {
        "text": (
            "It rings once, then you hear it — your own voice, mid-sentence, "
            "saying the exact words from the voicemail. "
            "Not a playback. Live. You're already saying them. "
            "You don't remember making this call. You don't remember picking up the phone."
        ),
        "scene_prompt": (
            "The player called the number and heard themselves already speaking — "
            "already recording the voicemail. They have no memory of initiating the call. "
            "The loop has already begun."
        ),
        "tone": "threshold",
        "choices": {
            "finish saying the warning": "end_loop",
            "hang up and run": "vm_check_door",
        },
        "arc": "confrontation",
    },

    "vm_ignore": {
        "text": (
            "You set the phone face-down. You tell yourself it was a prank, "
            "a glitch, someone's idea of a joke. "
            "The apartment is quiet. The door is locked. "
            "At 11:47, something knocks twice — the exact knock of someone who knows you'll recognize it."
        ),
        "scene_prompt": (
            "The player ignored the voicemail and tried to sleep. "
            "At 11:47 something knocked on their door — twice, "
            "in a pattern they recognize."
        ),
        "tone": "dread",
        "choices": {
            "check the peephole": "vm_check_door",
            "don't move, don't breathe": "vm_clock",
        },
        "arc": "confrontation",
    },

    "vm_clock": {
        "text": (
            "You sit in the dark and watch the clock. 11:51. 11:56. 11:59. "
            "Nothing knocks. Nothing moves. "
            "At midnight the voicemail deletes itself. "
            "In the morning you will not be certain it ever existed — "
            "except for the way your hands are shaking."
        ),
        "scene_prompt": (
            "The player waited in the dark through the final minutes before midnight. "
            "Nothing came. At midnight the voicemail deleted itself. "
            "By morning they are unsure it was real."
        ),
        "tone": "loss",
        "choices": {
            "check the door in the morning light": "end_safe",
            "never check": "end_static",
        },
        "arc": "resolution",
    },

    "vm_check_door": {
        "text": (
            "You look through the peephole. "
            "The hallway is empty — but the welcome mat has been moved six inches to the left. "
            "It has always faced the same direction. You checked obsessively when you moved in. "
            "Whoever was there is gone. They left that for you to find."
        ),
        "scene_prompt": (
            "The player checked the peephole and found the hallway empty. "
            "But the welcome mat has moved — subtly, deliberately. "
            "Someone was there and chose to leave a sign instead of entering."
        ),
        "tone": "threshold",
        "choices": {
            "open the door": "end_loop",
            "back away and wait for morning": "end_safe",
        },
        "arc": "resolution",
    },

    "end_safe": {
        "text": (
            "Morning comes. You made it through. "
            "You don't know what was outside, or what you were supposed to do, "
            "or who called. "
            "You only know this: your phone has no record of the voicemail. "
            "But it has one new outgoing call, placed at 3:12 AM, "
            "to a number with eleven digits."
        ),
        "scene_prompt": (
            "The player survived the night. But their phone now shows an outgoing call "
            "made at 3:12 AM to an eleven-digit number — a call they have no memory of making."
        ),
        "tone": "threshold",
        "choices": {
            "listen to the voicemail you left": "intro",
        },
        "arc": "end",
    },

    "end_loop": {
        "text": (
            "The words come out of you without choosing them. "
            "Your voice says: *don't answer the door tonight.* "
            "You don't know who you're calling. You don't know if they'll listen. "
            "You only know that someone must warn them — "
            "because no one warned you."
        ),
        "scene_prompt": (
            "The player has become the voice in the voicemail. "
            "They are now making the call, saying the warning, "
            "completing the loop. The cycle continues."
        ),
        "tone": "loss",
        "choices": {
            "begin the loop again": "intro",
        },
        "arc": "end",
    },

    "end_static": {
        "text": (
            "You decide the safest thing is to never be certain. "
            "You go to work. You eat lunch. You answer your emails. "
            "Three weeks later, someone asks if you're feeling alright — "
            "you've seemed different since that Tuesday. "
            "You have no memory of a Tuesday."
        ),
        "scene_prompt": (
            "The player chose not to engage with the mystery. "
            "Life continued normally — but something about them has subtly changed, "
            "and they have a gap in their memory."
        ),
        "tone": "loss",
        "choices": {
            "try to remember": "intro",
        },
        "arc": "end",
    },
}
