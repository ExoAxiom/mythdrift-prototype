ADVENTURE_META = {
    "id": "the_cartographer",
    "title": "The Cartographer",
    "genre": "Dark Mystery",
    "description": "A dying stranger leaves you a hand-drawn map. Your house is on it. The town it shows doesn't exist — until you drive toward it.",
    "estimated_minutes": 15,
    "type": "guided",
    "tags": ["mystery", "medium", "solo", "dark"],
    "use_authored_text": True,
}

LANDMARK_BEATS = {
    "cart_examines_map":   "studied the map carefully before deciding",
    "cart_church_helpful": "found the pastor willing to help",
    "cart_church_waiting": "found the pastor had been expecting them",
    "cart_drawer_opens":   "opened the locked drawer and found the journal",
    "cart_drawer_locked":  "the locked drawer refused them",
    "cart_cellar":         "descended into the cellar beneath their house on the map",
    "end_free":            "burned the map and walked away",
    "end_mapped":          "took the map and continued the cartographer's work",
    "end_forgotten":       "left the town and let it fade from memory",
}

STORY_GRAPH = {

    "intro": {
        "text": (
            "A man collapses on your doorstep at dusk. By the time the paramedics arrive he is gone. "
            "In his coat pocket: a hand-drawn map, folded into eighths, "
            "so worn the creases have become tears. "
            "Your house is on it. Labeled in someone else's handwriting, but the address is exact."
        ),
        "scene_prompt": (
            "A stranger has died on the player's doorstep. He left behind a hand-drawn map. "
            "The map shows their house, labeled precisely. The map depicts a town "
            "the player has never heard of."
        ),
        "tone": "discovery",
        "choices": {
            "examine the map carefully": "cart_examines_map",
            "call the police and hand it over": "cart_police",
            "find the town on the map": "cart_drive",
        },
        "arc": "discovery",
    },

    "cart_examines_map": {
        "text": (
            "You spread it on the kitchen table. The town is called Ardenvale — "
            "no search results, no record, no county that contains it. "
            "But the roads are real. You recognize three of them. "
            "They just don't connect the way they do on the map. "
            "Not yet."
        ),
        "scene_prompt": (
            "The player is examining the hand-drawn map. The town is called Ardenvale. "
            "It returns no search results. But the individual roads on the map are real — "
            "they just don't connect as shown. Not yet."
        ),
        "tone": "discovery",
        "choices": {
            "drive toward it": "cart_drive",
            "research the cartographer first": "cart_research",
        },
        "arc": "discovery",
    },

    "cart_police": {
        "text": (
            "You hand it over. The detective bags it without looking at it. "
            "Three days later you call to follow up — they have no record of the incident, "
            "no record of the map, no record of your call. "
            "But on your kitchen table, folded into eighths, the map has come back."
        ),
        "scene_prompt": (
            "The player tried to hand the map to police. All records of the incident vanished. "
            "The map returned to their kitchen table on its own."
        ),
        "tone": "dread",
        "choices": {
            "drive toward the town": "cart_drive",
            "burn the map": "cart_burn_early",
        },
        "arc": "discovery",
    },

    "cart_research": {
        "text": (
            "You find one reference: a local news article, 1987, about a cartographer "
            "named Elias Vorne who claimed to have discovered 'a town that only appears "
            "when someone goes looking for it.' He was institutionalized. "
            "He was released in 2019. The address on his discharge papers is yours."
        ),
        "scene_prompt": (
            "The player researched the cartographer. His name was Elias Vorne. "
            "He claimed the town only appears when someone looks for it. "
            "His last known address is the player's own home."
        ),
        "tone": "discovery",
        "choices": {
            "drive to the town": "cart_drive",
            "look for Vorne's records": "cart_examines_map",
        },
        "arc": "discovery",
    },

    "cart_burn_early": {
        "text": (
            "You burn it over the kitchen sink. The paper burns wrong — "
            "the smoke smells like rain and old wood, not paper. "
            "In the ash you can still make out the roads, the buildings, your house. "
            "The map remembers itself."
        ),
        "scene_prompt": (
            "The player tried to burn the map. It burned with the wrong smell. "
            "The ash retained the map's image — it remembers itself."
        ),
        "tone": "dread",
        "choices": {
            "drive toward the town": "cart_drive",
            "leave the ash and never look at it again": "end_forgotten",
        },
        "arc": "discovery",
    },

    "cart_drive": {
        "text": (
            "You follow the map. An hour out, the roads start to match it — "
            "intersections appearing where none were marked on your GPS, "
            "street signs you've never seen. "
            "A gas station attendant gives you directions without you asking. "
            "She doesn't look at you when she speaks."
        ),
        "scene_prompt": (
            "The player is driving toward the town. The roads are beginning to match the map. "
            "A gas station attendant gives them directions without being asked, "
            "without making eye contact."
        ),
        "tone": "dread",
        "choices": {
            "keep driving": "cart_town_entrance",
            "turn back": "end_forgotten",
        },
        "arc": "approach",
    },

    "cart_town_entrance": {
        "text": (
            "Ardenvale. Population: not listed. "
            "The town is small and almost right — like someone described a real town "
            "from memory and built it from the description. "
            "There is a church, a row of houses, and on the far end of the main road, "
            "a building with your name on the mailbox."
        ),
        "scene_prompt": (
            "The player has arrived in Ardenvale. The town is slightly off — like a replica. "
            "There is a church, houses, and at the end of the road, a building "
            "with the player's name on the mailbox."
        ),
        "tone": "threshold",
        "choices": {
            "go to the church": "cart_church",
            "go to your house on the map": "cart_your_house",
            "go to the building at the far end": "cart_office",
        },
        "arc": "town",
    },

    "cart_church": {
        "text": (
            "The church is unlocked. Inside, candles are burning for someone. "
            "A pastor emerges from the back — older, unhurried. "
            "He looks at you the way people look at something they've been waiting for."
        ),
        "scene_prompt": (
            "The player entered the church. Candles are burning. "
            "A pastor emerges and looks at them as though he has been expecting them."
        ),
        "tone": "threshold",
        "choices": {
            "ask him about the map": {
                "type": "rng",
                "outcomes": [
                    {"weight": 50, "next_beat_id": "cart_church_helpful"},
                    {"weight": 50, "next_beat_id": "cart_church_waiting"},
                ]
            },
            "ask him about Elias Vorne": "cart_church_vorne",
        },
        "arc": "town",
    },

    "cart_church_helpful": {
        "text": (
            "'Elias made this place,' the pastor says, simply. "
            "'He drew towns into existence. Ardenvale is the last one. "
            "He needed someone to finish the map — to find the office and look at what's inside.' "
            "He hands you a key. 'He said you'd come.'"
        ),
        "scene_prompt": (
            "The pastor revealed that Elias Vorne drew towns into existence. "
            "Ardenvale is his last. He gives the player a key to the cartographer's office "
            "and says Elias predicted they would come."
        ),
        "tone": "wonder",
        "choices": {
            "take the key and go to the office": "cart_office",
            "ask what finishing the map means": "cart_church_meaning",
        },
        "arc": "town",
    },

    "cart_church_waiting": {
        "text": (
            "The pastor doesn't answer your question. He asks one instead: "
            "'Do you know what you carry?' "
            "He's looking at your hands. You realize your fingers are stained — "
            "faintly, in the pattern of the map's roads, as though you drew it yourself."
        ),
        "scene_prompt": (
            "The pastor didn't answer about the map. He asked what the player carries. "
            "The player looks down and finds their fingers stained in the pattern "
            "of the map's roads — as if they drew it."
        ),
        "tone": "dread",
        "choices": {
            "go to the office": "cart_office",
            "go to your house on the map": "cart_your_house",
        },
        "arc": "town",
    },

    "cart_church_vorne": {
        "text": (
            "The pastor pauses. 'Elias came here the same way you did. "
            "He thought he was following someone else's map. "
            "Halfway through, he realized he'd drawn it himself — "
            "that morning, in his sleep, while his hands moved without him.'"
        ),
        "scene_prompt": (
            "The pastor explains that Elias Vorne also arrived following a map "
            "he didn't know he'd drawn himself — made in his sleep."
        ),
        "tone": "dread",
        "choices": {
            "go to the cartographer's office": "cart_office",
            "check your own hands": "cart_church_waiting",
        },
        "arc": "town",
    },

    "cart_church_meaning": {
        "text": (
            "'It means the town becomes permanent,' he says. 'Right now it exists "
            "only as long as you're here. When you leave, it folds. "
            "But if the last page of the map is completed — Ardenvale stays. "
            "Whether that's good depends entirely on what Ardenvale is for.'"
        ),
        "scene_prompt": (
            "The pastor explains that completing the map would make Ardenvale permanent. "
            "Currently it exists only while the player is present. "
            "What it exists for is unclear."
        ),
        "tone": "threshold",
        "choices": {
            "go to the office and look": "cart_office",
            "leave without finishing it": "end_forgotten",
        },
        "arc": "town",
    },

    "cart_your_house": {
        "text": (
            "The door is unlocked. Inside it is your house — "
            "your furniture, your photos, your books in the right order. "
            "But the photos show places you've never been. "
            "And the books are in a language you can almost read."
        ),
        "scene_prompt": (
            "The player entered the house with their name on the mailbox. "
            "It is their home — but with photos of places they've never been "
            "and books in a language they nearly understand."
        ),
        "tone": "wonder",
        "choices": {
            "look at the photos": "cart_photos",
            "go to the cellar": "cart_cellar",
            "leave and go to the office": "cart_office",
        },
        "arc": "town",
    },

    "cart_photos": {
        "text": (
            "The photos show twelve towns — all of them slightly wrong in the same way. "
            "All of them with a building at the far end of the main road. "
            "In the last photo, the building has your name on the mailbox. "
            "You are standing in front of it, smiling, in a coat you've never owned."
        ),
        "scene_prompt": (
            "The photos show twelve towns like Ardenvale, each with a building at the far end. "
            "In the final photo the player stands in front of it, "
            "smiling, in a coat they've never owned."
        ),
        "tone": "dread",
        "choices": {
            "go to the cellar": "cart_cellar",
            "go to the cartographer's office now": "cart_office",
        },
        "arc": "town",
    },

    "cart_cellar": {
        "text": (
            "The cellar contains twelve filing cabinets. "
            "Each one is labeled with a town name. "
            "One of them is labeled Ardenvale, and inside it: one file. "
            "Your name, your address, and a single handwritten note: "
            "*You will finish what Elias started.*"
        ),
        "scene_prompt": (
            "The cellar has twelve filing cabinets, one per town. "
            "The Ardenvale cabinet has one file — the player's name, address, "
            "and a note: 'You will finish what Elias started.'"
        ),
        "tone": "dread",
        "choices": {
            "take the file and go to the office": "cart_office",
            "put the file back and leave Ardenvale": "end_forgotten",
        },
        "arc": "town",
    },

    "cart_office": {
        "text": (
            "The cartographer's office is the last door on the main road. "
            "Inside: a drafting table, twelve completed maps on the walls, "
            "and one unfinished. The unfinished one is Ardenvale. "
            "In the center of the map, where the cartographer's office should be, "
            "there is a locked drawer in the table."
        ),
        "scene_prompt": (
            "The cartographer's office has twelve completed maps and one unfinished — Ardenvale. "
            "The drafting table has a locked drawer where the office itself should be on the map."
        ),
        "tone": "threshold",
        "choices": {
            "try to open the drawer": {
                "type": "rng",
                "outcomes": [
                    {"weight": 60, "next_beat_id": "cart_drawer_opens"},
                    {"weight": 40, "next_beat_id": "cart_drawer_locked"},
                ]
            },
            "study the unfinished map first": "cart_studies_map",
        },
        "arc": "truth",
    },

    "cart_studies_map": {
        "text": (
            "The map of Ardenvale is nearly complete. Every building, every road. "
            "One thing is missing: the cartographer's office itself is a blank. "
            "There is a pen on the table. "
            "You understand that you are being asked to draw the room you are standing in."
        ),
        "scene_prompt": (
            "The player studies the unfinished map of Ardenvale. "
            "Everything is drawn except the cartographer's office. "
            "A pen sits on the table. They understand they are meant to complete it."
        ),
        "tone": "threshold",
        "choices": {
            "try the locked drawer first": {
                "type": "rng",
                "outcomes": [
                    {"weight": 60, "next_beat_id": "cart_drawer_opens"},
                    {"weight": 40, "next_beat_id": "cart_drawer_locked"},
                ]
            },
            "pick up the pen and draw": "cart_truth_revealed",
        },
        "arc": "truth",
    },

    "cart_drawer_opens": {
        "text": (
            "The drawer opens easily, as if it was never truly locked — just waiting. "
            "Inside: Elias Vorne's journal, open to the final entry. "
            "It reads: 'The town only becomes real when someone draws the last room. "
            "I couldn't do it. I kept drawing myself out of the picture. "
            "I hope you are braver than I am.'"
        ),
        "scene_prompt": (
            "The locked drawer opened. Inside is Elias Vorne's journal open to his final entry. "
            "He explains the town becomes real when someone draws the last room. "
            "He couldn't do it. He hopes the player is braver."
        ),
        "tone": "discovery",
        "choices": {
            "pick up the pen and complete the map": "cart_truth_revealed",
            "take the journal and leave without drawing": "end_forgotten",
        },
        "arc": "truth",
    },

    "cart_drawer_locked": {
        "text": (
            "The drawer doesn't open. It doesn't budge, rattle, or respond. "
            "But as you pull, you notice: the pen on the table has rolled to the edge. "
            "The map of Ardenvale has shifted — the blank space for the office is larger now. "
            "The town wants to be completed more than it wants to be understood."
        ),
        "scene_prompt": (
            "The locked drawer refused to open. But the pen rolled toward the player "
            "and the blank on the map has grown. The town is asking to be completed."
        ),
        "tone": "dread",
        "choices": {
            "pick up the pen and draw": "cart_truth_revealed",
            "leave without completing anything": "end_forgotten",
        },
        "arc": "truth",
    },

    "cart_truth_revealed": {
        "text": (
            "You pick up the pen. You draw the room. The walls, the table, the maps. "
            "The window. The pen. Yourself, drawing. "
            "When you finish, the room changes — solidifies, like something that was held "
            "on a single breath finally exhaled. "
            "Ardenvale is now permanent. You made it real."
        ),
        "scene_prompt": (
            "The player completed the map by drawing the cartographer's office — "
            "including themselves, drawing. The room solidified. Ardenvale is now permanent."
        ),
        "tone": "threshold",
        "choices": {
            "burn the map and leave": "end_free",
            "take the map and keep going": "end_mapped",
            "leave the map here and walk away": "end_forgotten",
        },
        "arc": "resolution",
    },

    "end_free": {
        "text": (
            "You burn the map in the drafting table's metal tray. "
            "This time it burns correctly — paper burning, nothing else. "
            "When you drive out of Ardenvale, it doesn't follow you. "
            "It stays behind, permanent, real, existing on its own now. "
            "You are free. You hope it's a good town."
        ),
        "scene_prompt": (
            "The player burned the map. Ardenvale remains — permanent and real — "
            "but the player is free of it. They leave without being followed."
        ),
        "tone": "loss",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },

    "end_mapped": {
        "text": (
            "You take the map. All thirteen of them — Ardenvale and the twelve completed towns "
            "from the walls. In the car you understand what Elias Vorne was doing: "
            "drawing places into existence so that people who need somewhere to be "
            "will have somewhere to go. "
            "You wonder how many more are waiting."
        ),
        "scene_prompt": (
            "The player took all thirteen maps and left with Elias Vorne's purpose: "
            "to draw more towns into existence for people who need a place to be."
        ),
        "tone": "wonder",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },

    "end_forgotten": {
        "text": (
            "You leave. An hour down the road, you can't remember the name of the town. "
            "Two hours out, you can't remember the turn you took. "
            "By the time you get home, you remember a man dying on your doorstep "
            "and nothing else. "
            "Your kitchen table is clean. Your hands are stained with something faint and ink-dark."
        ),
        "scene_prompt": (
            "The player left without completing the map. The memories of Ardenvale faded "
            "during the drive home. Only ink-dark stains on their hands remain."
        ),
        "tone": "loss",
        "choices": {
            "drift again": "intro",
        },
        "arc": "end",
    },
}
