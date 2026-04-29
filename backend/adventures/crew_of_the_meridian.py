ADVENTURE_META = {
    "id": "crew_of_the_meridian",
    "title": "Crew of the Meridian",
    "genre": "Cosmic Sci-Fi",
    "description": "You wake alone on a deep-space research vessel. The logs say the crew left voluntarily. The distress beacon has been running for eleven years.",
    "estimated_minutes": 30,
    "type": "guided",
    "tags": ["sci-fi", "long", "cosmic", "mystery", "solo"],
}

LANDMARK_BEATS = {
    "mer_survivor_found":     "found the one remaining crew member",
    "mer_what_got_loose":     "discovered what escaped from containment",
    "mer_crew_vote":          "read the crew's final vote",
    "mer_transmission_sent":  "transmitted the findings",
    "mer_transmission_empty": "transmitted into silence",
    "end_broadcast":          "sent everything out into the dark",
    "end_remains":            "chose to stay aboard the Meridian",
    "end_silence":            "purged the logs and left nothing behind",
    "end_waiting":            "sent the signal and waited",
}

STORY_GRAPH = {

    # ─── WAKE ───────────────────────────────────────────────────────────────

    "intro": {
        "text": (
            "You wake in a research bunk you don't remember lying down in. "
            "The Meridian is running on reserve power — emergency amber, the hum of "
            "life support doing its minimum. "
            "The crew roster on the wall shows fourteen names. "
            "Twelve have a line through them. "
            "One says: YOU. The last one has no name at all."
        ),
        "scene_prompt": (
            "The player has woken alone on the research vessel Meridian. "
            "Emergency power only. The crew roster shows 14 names: 12 crossed out, "
            "one is the player's, one has no name."
        ),
        "tone": "discovery",
        "choices": {
            "go to the bridge": "mer_bridge",
            "check the other bunks": "mer_bunks",
            "look at the crew roster more carefully": "mer_roster",
        },
        "arc": "wake",
    },

    "mer_roster": {
        "text": (
            "The twelve crossed-out names all have dates — ranging over eleven years. "
            "They didn't leave at once. They left one at a time. "
            "Some departures are spaced days apart. Some years. "
            "The last crossing-out was fourteen months ago. "
            "Your name was added after that."
        ),
        "scene_prompt": (
            "The crew roster shows departures spread over eleven years, one at a time. "
            "The player's name was added fourteen months after the last departure."
        ),
        "tone": "dread",
        "choices": {
            "go to the bridge": "mer_bridge",
            "check the bunks for whoever has no name": "mer_bunks",
        },
        "arc": "wake",
    },

    "mer_bunks": {
        "text": (
            "Twelve bunks. Eleven are stripped — no sheets, no personal items, "
            "no sign that anyone chose to leave something behind. "
            "The twelfth bunk has sheets, a photograph face-down, and a meal "
            "half-eaten on the side table. The food hasn't spoiled. "
            "It is still warm."
        ),
        "scene_prompt": (
            "Eleven bunks are stripped bare. The twelfth has sheets, a face-down photo, "
            "and a still-warm half-eaten meal."
        ),
        "tone": "dread",
        "choices": {
            "turn over the photograph": "mer_photo",
            "go to the bridge immediately": "mer_bridge",
            "check the meal for a date": "mer_bridge",
        },
        "arc": "wake",
    },

    "mer_photo": {
        "text": (
            "The photograph shows the Meridian's crew — all fourteen, in a common room "
            "that no longer looks like any room on the ship you can see. "
            "Everyone is smiling. Your face is in the back row. "
            "You have no memory of this photograph being taken."
        ),
        "scene_prompt": (
            "The photograph shows all 14 crew members including the player, smiling. "
            "The room in the photo doesn't match any room on the ship. "
            "The player has no memory of this photo."
        ),
        "tone": "dread",
        "choices": {
            "go to the bridge": "mer_bridge",
            "look for the room in the photograph": "mer_bridge",
        },
        "arc": "wake",
    },

    # ─── BRIDGE ─────────────────────────────────────────────────────────────

    "mer_bridge": {
        "text": (
            "The bridge is intact and unmanned. Navigation shows the Meridian "
            "holding a slow orbit around a body with no designation — "
            "no name, no classification, just coordinates and a note: *do not approach.* "
            "The distress beacon has been transmitting for 4,051 days. "
            "Eleven years, one month, three days."
        ),
        "scene_prompt": (
            "The bridge is running. The Meridian orbits an undesignated body marked 'do not approach.' "
            "The distress beacon has been running for 4,051 days."
        ),
        "tone": "wonder",
        "choices": {
            "read the ship's logs": "mer_logs",
            "go to engineering": "mer_engineering",
            "go to the crew quarters and lab section": "mer_crew_quarters",
            "go to the communications room": "mer_comms",
        },
        "arc": "investigation",
    },

    "mer_logs": {
        "text": (
            "The log entries for the first three years are routine — samples, readings, "
            "maintenance notes, birthdays celebrated in the common room. "
            "Year four: one entry marked CLASSIFIED, access revoked. "
            "Year four, two weeks later: the first crew member requests departure. "
            "The log simply says she was accommodated."
        ),
        "scene_prompt": (
            "The ship's logs are routine for three years. Year four has a classified entry, "
            "then the first departure two weeks later. The log says she was 'accommodated.'"
        ),
        "tone": "discovery",
        "choices": {
            "try to access the classified entry": "mer_classified",
            "read the later logs": "mer_late_logs",
            "go to engineering": "mer_engineering",
        },
        "arc": "investigation",
    },

    "mer_classified": {
        "text": (
            "Clearance denied. But the denial message includes a field: *Authorized by:* "
            "and the name listed is yours. "
            "You classified this entry. You don't remember doing it. "
            "Below the denial, in the notes field, your own handwriting: "
            "*Don't read this yet. You're not ready.*"
        ),
        "scene_prompt": (
            "The classified log was sealed by the player themselves. "
            "A note in their own handwriting says: 'Don't read this yet. You're not ready.'"
        ),
        "tone": "dread",
        "choices": {
            "override your own clearance": "mer_classified_read",
            "leave it and read the other logs": "mer_late_logs",
        },
        "arc": "investigation",
    },

    "mer_classified_read": {
        "text": (
            "The entry is six words: *It is not from out there.* "
            "Below, an addendum, dated four years later, in shakier handwriting: "
            "*It was already here. On us. Has been for longer than the mission.*"
        ),
        "scene_prompt": (
            "The classified log says: 'It is not from out there.' "
            "A later addendum: 'It was already here. On us. Has been for longer than the mission.'"
        ),
        "tone": "dread",
        "choices": {
            "go to the lab section": "mer_lab",
            "go to engineering to understand the ship's status": "mer_engineering",
        },
        "arc": "investigation",
    },

    "mer_late_logs": {
        "text": (
            "The later logs are sparse. Year seven: 'Another departure. Accommodated.' "
            "Year nine: 'Three this month. The beacon stays on.' "
            "Year eleven: 'One left. Then the one with no name arrived. "
            "I don't know where they came from. They seem to know the ship.'"
        ),
        "scene_prompt": (
            "Later logs show departures through year eleven. The final entry: "
            "'One left. Then the one with no name arrived. They seem to know the ship.'"
        ),
        "tone": "dread",
        "choices": {
            "search for the unnamed crew member": "mer_survivor",
            "go to the lab section": "mer_lab",
        },
        "arc": "investigation",
    },

    # ─── ENGINEERING ────────────────────────────────────────────────────────

    "mer_engineering": {
        "text": (
            "Engineering is running on automatic. The power core is stable — "
            "more stable than it should be at this age, as though it has been "
            "carefully maintained by someone who understood it very well. "
            "There are two things worth examining: the fuel logs, and a maintenance "
            "shaft someone has sealed from the inside."
        ),
        "scene_prompt": (
            "Engineering is in good condition — suspiciously well-maintained. "
            "The fuel logs and a sealed maintenance shaft are the two points of interest."
        ),
        "tone": "discovery",
        "choices": {
            "read the fuel logs": "mer_fuel_logs",
            "open the sealed maintenance shaft": "mer_shaft",
        },
        "arc": "investigation",
    },

    "mer_fuel_logs": {
        "text": (
            "The Meridian has enough fuel for sixty more years of orbit. "
            "It had enough for a five-year mission. "
            "The logs show no resupply. The fuel simply stopped depleting "
            "in year three — the same year as the classified entry."
        ),
        "scene_prompt": (
            "The Meridian's fuel stopped depleting in year three — the same year as the classified log. "
            "It now has fuel for sixty more years with no resupply."
        ),
        "tone": "wonder",
        "choices": {
            "open the maintenance shaft": "mer_shaft",
            "go to the lab section": "mer_lab",
            "go to the bridge": "mer_bridge",
        },
        "arc": "investigation",
    },

    "mer_shaft": {
        "text": (
            "The shaft opens from outside — you have to unscrew the cover. "
            "Inside, curled into the narrow space: a person, alive, asleep. "
            "Their crew ID is clipped to their collar. It reads: *UNNAMED — DO NOT WAKE.*"
        ),
        "scene_prompt": (
            "Inside the sealed maintenance shaft is a living person, asleep. "
            "Their ID says: UNNAMED — DO NOT WAKE."
        ),
        "tone": "threshold",
        "choices": {
            "wake them": {
                "type": "rng",
                "outcomes": [
                    {"weight": 30, "next_beat_id": "mer_survivor_coherent"},
                    {"weight": 50, "next_beat_id": "mer_survivor_delusional"},
                    {"weight": 20, "next_beat_id": "mer_survivor_gone"},
                ]
            },
            "leave them and find another way": "mer_lab",
        },
        "arc": "investigation",
    },

    "mer_survivor_found": {
        "text": "",  # placeholder — handled by sub-beats
        "scene_prompt": "",
        "tone": "discovery",
        "choices": {"continue": "mer_lab"},
        "arc": "investigation",
    },

    "mer_survivor_coherent": {
        "text": (
            "They wake slowly and look at you without surprise. "
            "'You're the last one,' they say. 'Good. I was starting to think you wouldn't come.' "
            "They climb out stiffly. 'I've been keeping the ship running. "
            "Someone had to. The others — they all had reasons to go. "
            "I didn't have anywhere to go *to.*'"
        ),
        "scene_prompt": (
            "The unnamed crew member wakes and is coherent. They've been maintaining the ship. "
            "They say the player is 'the last one' and seem to have been waiting. "
            "They stayed because they had nowhere to go."
        ),
        "tone": "discovery",
        "choices": {
            "ask what happened to the crew": "mer_crew_vote",
            "ask what they are keeping from": "mer_classified_read",
            "go together to the lab": "mer_lab",
        },
        "arc": "investigation",
    },

    "mer_survivor_delusional": {
        "text": (
            "They wake screaming. Three words, over and over: *it's still counting.* "
            "When they see you, they stop. They study your face for a long time. "
            "'You're new,' they say finally. 'That means they sent you. "
            "That means it's almost time.' They won't say what is almost time."
        ),
        "scene_prompt": (
            "The unnamed crew member woke screaming 'it's still counting.' "
            "Seeing the player, they calmed and said 'you're new, they sent you, it's almost time.' "
            "They won't clarify."
        ),
        "tone": "dread",
        "choices": {
            "go to the lab section to understand": "mer_lab",
            "ask about the vote the logs mentioned": "mer_crew_vote",
        },
        "arc": "investigation",
    },

    "mer_survivor_gone": {
        "text": (
            "They wake, look at you, and say one sentence: "
            "'The lab. Section C. Don't touch the walls.' "
            "Then they close their eyes and are gone — not dead, but gone, "
            "the way a light goes off. The maintenance shaft closes itself."
        ),
        "scene_prompt": (
            "The unnamed crew member woke, said 'lab, section C, don't touch the walls,' "
            "then went silent. Not dead — just gone. The shaft closed itself."
        ),
        "tone": "dread",
        "choices": {
            "go to section C of the lab": "mer_lab_section_c",
            "go to the lab and proceed carefully": "mer_lab",
        },
        "arc": "investigation",
    },

    "mer_crew_vote": {
        "text": (
            "The crew voted, in year four, on whether to report what they found. "
            "Eleven voted yes. Three voted no. "
            "Then, one by one, over years, the yes votes began to leave — "
            "not forcibly, but willingly, as though they'd concluded "
            "that reporting it wasn't possible. The no votes stayed longest."
        ),
        "scene_prompt": (
            "The crew voted in year four on whether to report their discovery. "
            "Eleven voted yes, three no. Over years, the yes-voters left. "
            "The no-voters stayed longest."
        ),
        "tone": "discovery",
        "choices": {
            "go to the lab to find out what they voted about": "mer_lab",
            "go to communications to see if any reports were sent": "mer_comms",
        },
        "arc": "investigation",
    },

    # ─── CREW QUARTERS / LAB ────────────────────────────────────────────────

    "mer_crew_quarters": {
        "text": (
            "The crew quarters hold eleven stripped bunks and one occupied one. "
            "The lab section is adjacent — sealed behind a door labeled "
            "SECTION C: RESTRICTED, BIOLOGICAL MATERIAL. "
            "A supply hatch in the corridor is padlocked."
        ),
        "scene_prompt": (
            "The crew quarters show eleven stripped bunks and one occupied. "
            "Adjacent is the lab — Section C, restricted. "
            "A padlocked supply hatch is in the corridor."
        ),
        "tone": "discovery",
        "choices": {
            "go to the lab section": "mer_lab",
            "check the supply hatch": {
                "type": "rng",
                "outcomes": [
                    {"weight": 55, "next_beat_id": "mer_supply_stocked"},
                    {"weight": 45, "next_beat_id": "mer_supply_stripped"},
                ]
            },
        },
        "arc": "investigation",
    },

    "mer_supply_stocked": {
        "text": (
            "The hatch opens onto a storeroom still fully stocked — "
            "emergency rations, medical supplies, two environment suits. "
            "Someone prepared this for a long stay, or a long wait. "
            "On the shelf, tagged with your name: a small notebook. "
            "The pages are blank except for the last one: *Trust the beacon.*"
        ),
        "scene_prompt": (
            "The supply hatch is fully stocked. Someone prepared it for a long stay. "
            "A notebook tagged with the player's name has one entry: 'Trust the beacon.'"
        ),
        "tone": "discovery",
        "choices": {
            "go to the lab section": "mer_lab",
            "go to communications about the beacon": "mer_comms",
        },
        "arc": "investigation",
    },

    "mer_supply_stripped": {
        "text": (
            "The hatch opens onto an empty room — bare shelves, "
            "dust outlines where equipment used to be. "
            "Someone took everything. "
            "On the floor, in the dust: a word traced with a finger. "
            "*Don't.*"
        ),
        "scene_prompt": (
            "The supply hatch is completely stripped. Everything removed. "
            "In the dust, someone traced one word with a finger: 'Don't.'"
        ),
        "tone": "dread",
        "choices": {
            "go to the lab anyway": "mer_lab",
            "go to the bridge and reconsider": "mer_bridge",
        },
        "arc": "investigation",
    },

    "mer_lab": {
        "text": (
            "The lab is divided into sections A through D. "
            "A and B are standard — samples, cultures, research terminals. "
            "Section C's door has been welded shut from the outside. "
            "Section D is open and appears undisturbed except for one thing: "
            "every sample container on the wall is empty."
        ),
        "scene_prompt": (
            "The lab has four sections. A and B are normal. Section C is welded shut. "
            "Section D is open but all sample containers are empty."
        ),
        "tone": "threshold",
        "choices": {
            "read the research files in section D": "mer_research_files",
            "try to open section C": {
                "type": "rng",
                "outcomes": [
                    {"weight": 40, "next_beat_id": "mer_containment_dormant"},
                    {"weight": 60, "next_beat_id": "mer_containment_active"},
                ]
            },
            "go to section C specifically": "mer_lab_section_c",
        },
        "arc": "investigation",
    },

    "mer_lab_section_c": {
        "text": (
            "Section C is where the weld is. Up close, you can hear it — "
            "not sound exactly, more like pressure. "
            "Like something on the other side is leaning against the door "
            "with its full weight, patiently, without urgency."
        ),
        "scene_prompt": (
            "Section C is welded shut. Close up, there's a pressure — "
            "like something leaning against the door from the other side, patiently."
        ),
        "tone": "dread",
        "choices": {
            "open it": {
                "type": "rng",
                "outcomes": [
                    {"weight": 40, "next_beat_id": "mer_containment_dormant"},
                    {"weight": 60, "next_beat_id": "mer_containment_active"},
                ]
            },
            "leave it welded and go to section D": "mer_research_files",
        },
        "arc": "investigation",
    },

    "mer_research_files": {
        "text": (
            "The research files are eleven years of data on something "
            "the crew called simply 'the presence.' "
            "It doesn't have mass or temperature. It has *preference.* "
            "It prefers certain crew members to others. "
            "It preferred the ones who left. "
            "It seems to be helping them go."
        ),
        "scene_prompt": (
            "The research files describe 'the presence' — no mass or temperature, "
            "but preferences. It preferred certain crew members and seemed to help them depart."
        ),
        "tone": "wonder",
        "choices": {
            "try to open section C": {
                "type": "rng",
                "outcomes": [
                    {"weight": 40, "next_beat_id": "mer_containment_dormant"},
                    {"weight": 60, "next_beat_id": "mer_containment_active"},
                ]
            },
            "go to communications with this information": "mer_comms",
        },
        "arc": "investigation",
    },

    "mer_containment_dormant": {
        "text": (
            "Section C opens without resistance. Inside: empty. "
            "No samples, no equipment, no evidence of whatever was here. "
            "But the air is different — denser, older, "
            "like breathing in a room that has been sealed for a very long time. "
            "In the center of the floor, a single handprint. Not human."
        ),
        "scene_prompt": (
            "Section C is empty but for old air and a single non-human handprint on the floor. "
            "Whatever was here is gone."
        ),
        "tone": "wonder",
        "choices": {
            "take a sample of the air": "mer_comms",
            "document the handprint and go to communications": "mer_comms",
        },
        "arc": "investigation",
    },

    "mer_what_got_loose": {
        "text": "",  # handled by active branch
        "scene_prompt": "",
        "tone": "dread",
        "choices": {"continue": "mer_comms"},
        "arc": "investigation",
    },

    "mer_containment_active": {
        "text": (
            "The weld breaks and the door opens and there is nothing there — "
            "and then you realize you are looking at it wrong. "
            "It isn't visible. It is the thing that makes the visible make sense. "
            "You can feel it noticing you. "
            "Then: a sound, low, almost like language, and a feeling "
            "like a question being asked in a frequency your body understands but your mind can't."
        ),
        "scene_prompt": (
            "Section C opened and the presence is inside — invisible, but perceptible. "
            "It notices the player. It asks something in a frequency the body understands "
            "but the mind cannot process."
        ),
        "tone": "wonder",
        "choices": {
            "answer the question": "mer_answers",
            "back away to communications": "mer_comms",
        },
        "arc": "investigation",
    },

    "mer_answers": {
        "text": (
            "You don't know what you say. Your body answers without you. "
            "The presence seems satisfied. "
            "When it pulls back, you feel lighter — not because something left, "
            "but because something that was pressing was released. "
            "You understand: it has been waiting for permission."
        ),
        "scene_prompt": (
            "The player's body answered the presence's question without conscious thought. "
            "The presence is satisfied — it was waiting for permission. Something has been released."
        ),
        "tone": "threshold",
        "choices": {
            "go to communications": "mer_comms",
        },
        "arc": "investigation",
    },

    # ─── COMMUNICATIONS ──────────────────────────────────────────────────────

    "mer_comms": {
        "text": (
            "The communications room is fully operational. "
            "The outgoing queue has one item — a report, fully written, "
            "encrypted, addressed to a research authority. "
            "The author field is blank. "
            "The last incoming message is from eleven years ago, acknowledging the distress beacon "
            "and stating that a vessel has been dispatched."
        ),
        "scene_prompt": (
            "The comms room has a complete encrypted report queued to send — author field blank. "
            "The last incoming message, eleven years ago, said a vessel was dispatched. "
            "It never arrived."
        ),
        "tone": "threshold",
        "choices": {
            "read the queued report before sending": "mer_reads_report",
            "send the report immediately": "mer_transmission",
            "read the last incoming message": "mer_last_message",
        },
        "arc": "decision",
    },

    "mer_last_message": {
        "text": (
            "The incoming message is from a Coordinator Vielle, signed off efficiently: "
            "'Distress received. Vessel dispatched. ETA 14 days.' "
            "Eleven years ago. "
            "Below, in the margin, handwritten on the printed copy: "
            "*No one came. We stopped expecting them in year two.*"
        ),
        "scene_prompt": (
            "The last incoming message promised rescue in 14 days, eleven years ago. "
            "A handwritten note on the printed copy: 'No one came. We stopped expecting them in year two.'"
        ),
        "tone": "loss",
        "choices": {
            "send the queued report": "mer_transmission",
            "read the queued report first": "mer_reads_report",
            "purge the queue and leave": "end_silence",
        },
        "arc": "decision",
    },

    "mer_reads_report": {
        "text": (
            "The report details everything — the presence, the departures, the preference system, "
            "the handprint, the fuel anomaly, the classified entry. "
            "It is precise, thorough, and written in your voice. "
            "The conclusion: *The presence is not hostile. It is a guide. "
            "The crew did not leave because they were taken. They left because they were ready.*"
        ),
        "scene_prompt": (
            "The queued report is written in the player's voice. It concludes: "
            "'The presence is not hostile. It is a guide. The crew left because they were ready.'"
        ),
        "tone": "wonder",
        "choices": {
            "send it": "mer_transmission",
            "add to it": "mer_transmission",
            "purge it": "end_silence",
            "stay and keep the beacon running": "end_remains",
        },
        "arc": "decision",
    },

    "mer_transmission": {
        "text": (
            "You transmit."
        ),
        "scene_prompt": "The player initiates the transmission.",
        "tone": "threshold",
        "choices": {
            "watch the signal go out": {
                "type": "rng",
                "outcomes": [
                    {"weight": 60, "next_beat_id": "mer_transmission_sent"},
                    {"weight": 40, "next_beat_id": "mer_transmission_empty"},
                ]
            },
        },
        "arc": "decision",
    },

    "mer_transmission_sent": {
        "text": (
            "The signal goes. Thirty-eight seconds later — far too fast for the distance — "
            "an acknowledgment comes back. Two words: *Understood. Continue.* "
            "No vessel dispatched. No instructions. Just: continue."
        ),
        "scene_prompt": (
            "The transmission was acknowledged in 38 seconds — impossibly fast. "
            "The reply: 'Understood. Continue.' No vessel, no instructions."
        ),
        "tone": "threshold",
        "choices": {
            "stay and continue": "end_remains",
            "send everything and leave": "end_broadcast",
            "purge the logs and go": "end_silence",
        },
        "arc": "resolution",
    },

    "mer_transmission_empty": {
        "text": (
            "The signal goes and nothing comes back. "
            "You watch the transmission tracker for an hour. "
            "The signal is still traveling — clean, unobstructed, outward. "
            "No acknowledgment. "
            "Either no one is listening, or what is listening is not the kind of thing "
            "that sends acknowledgments."
        ),
        "scene_prompt": (
            "The signal went out cleanly but nothing came back after an hour. "
            "Either no one is listening, or what listens doesn't reply."
        ),
        "tone": "loss",
        "choices": {
            "send the rescue signal anyway": {
                "type": "rng",
                "outcomes": [
                    {"weight": 60, "next_beat_id": "mer_transmission_sent"},
                    {"weight": 40, "next_beat_id": "end_waiting"},
                ]
            },
            "stay aboard and wait": "end_remains",
            "purge everything and go": "end_silence",
        },
        "arc": "resolution",
    },

    # ─── ENDINGS ─────────────────────────────────────────────────────────────

    "end_broadcast": {
        "text": (
            "You broadcast everything — the report, the logs, the research files, "
            "the recording of the presence, the handprint measurements. "
            "All of it, on every frequency, continuously. "
            "Then you take the escape pod and go. "
            "Behind you, the Meridian keeps broadcasting. "
            "You don't know who will hear it. You decide that's not your question to answer."
        ),
        "scene_prompt": (
            "The player broadcast all findings on every frequency, then left. "
            "The Meridian continues broadcasting. They've decided who hears it is not their concern."
        ),
        "tone": "defiance",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },

    "end_remains": {
        "text": (
            "You stay. "
            "You maintain the power core, tend the beacon, eat from the supplies, "
            "read the eleven years of research, and wait. "
            "The presence visits sometimes — you feel it as a warmth, a patience. "
            "You begin to understand what the crew understood, one by one, "
            "before they were ready to go. "
            "You are not ready yet."
        ),
        "scene_prompt": (
            "The player chose to stay aboard the Meridian. They tend the ship and wait. "
            "The presence visits. They begin to understand what the crew understood "
            "before leaving. They are not ready yet."
        ),
        "tone": "wonder",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },

    "end_silence": {
        "text": (
            "You purge the logs. Every record, every report, every research file. "
            "The beacon goes off. "
            "You take the escape pod and go, and behind you the Meridian "
            "drifts in its clean orbit, carrying nothing. "
            "Whatever happened here happened only to the people who were here. "
            "You decide that is how it should stay."
        ),
        "scene_prompt": (
            "The player purged all records and silenced the beacon before leaving. "
            "The Meridian drifts, empty and clean. "
            "What happened here stays only with those who were there."
        ),
        "tone": "loss",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },

    "end_waiting": {
        "text": (
            "You send the rescue signal and wait. "
            "Days pass. Then weeks. The supplies are adequate. "
            "The presence keeps you company in its way. "
            "One morning the long-range sensors catch something — "
            "a vessel, incoming, still too far to identify. "
            "It's been eleven years since anyone came. "
            "You make sure the beacon is clear and bright and wait to see "
            "who finally answered."
        ),
        "scene_prompt": (
            "The player sent the rescue signal and waited. After weeks, sensors detected "
            "an incoming vessel — still too far to identify. The first response in eleven years."
        ),
        "tone": "threshold",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },
}
