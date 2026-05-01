"""
seed.py - Populates all reference / lookup tables with initial data.
Run once: python database/seed.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.models import get_db, init_db

LOOKUP_SEED_DATA = {
    "CharacterClass": [
        {"ClassName": "Warrior",      "Description": "A powerful melee fighter."},
        {"ClassName": "Rogue",        "Description": "A stealthy assassin skilled with daggers."},
        {"ClassName": "Paladin",      "Description": "A holy knight sworn to justice."},
        {"ClassName": "Necromancer",  "Description": "A master of death magic."},
        {"ClassName": "Ranger",       "Description": "A skilled archer and wilderness tracker."},
        {"ClassName": "Berserker",    "Description": "A furious warrior driven by rage."}
    ],
    "Species": [
        {"SpeciesName": "Human"},
        {"SpeciesName": "Dwarf"},
        {"SpeciesName": "Elf"},
        {"SpeciesName": "Orc"},
        {"SpeciesName": "Halfling"},
        {"SpeciesName": "Dragonborn"}

    ],
    "Alignment": [
        {"AlignmentName": "Lawful Good"},
        {"AlignmentName": "Neutral"},
        {"AlignmentName": "Chaotic Good"},
        {"AlignmentName": "Lawful Evil"},
        {"AlignmentName": "Chaotic Neutral"},
    ],
    "ItemType": [
        {"TypeName": "Weapon"},
        {"TypeName": "Potion"},
        {"TypeName": "Armor"},
        {"TypeName": "Artifact"},
        {"TypeName": "Scroll"},
    ],
    "Rarity": [
        {"RarityName": "Common"},
        {"RarityName": "Uncommon"},
        {"RarityName": "Rare"},
        {"RarityName": "Epic"},
        {"RarityName": "Legendary"},
    ],
    "Region": [
        {"RegionName": "The Verdant Vale"},
        {"RegionName":"Defend the Vale"},
        {"RegionName":"Shadowfen Marshes"},
        {"RegionName":"Ashpeak Mountains"},
        {"RegionName":"Whispering Woods"},
        {"RegionName":"Stormbreak Coast"},

    ],
    "Difficulty": [
        {"DifficultyName": "Novice"},
        {"DifficultyName": "Journeyman"},
        {"DifficultyName": "Expert"},
        {"DifficultyName": "Master"},
        {"DifficultyName": "Legendary"},
    ],
}


def table_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) AS Total FROM {table_name}")
    return cursor.fetchone()["Total"]


def fetch_lookup_map(cursor, table_name, key_field):
    cursor.execute(f"SELECT * FROM {table_name}")
    return {row[key_field]: dict(row) for row in cursor.fetchall()}


def seed_lookup_tables(cursor):
    for table_name, rows in LOOKUP_SEED_DATA.items():
        if table_count(cursor, table_name) == 0:
            for row in rows:
                columns      = ", ".join(row.keys())
                placeholders = ", ".join(["?"] * len(row))
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                    tuple(row.values())
                )
            print(f"  ✔ Seeded {table_name}")
        else:
            print(f"  – Skipped {table_name} (already has data)")


def seed_core_data(cursor):
    if table_count(cursor, "Character") > 0:
        print("  – Skipped Character / Item / Quest / Inventory / CharacterQuest (already has data)")
        return

    classes    = fetch_lookup_map(cursor, "CharacterClass", "ClassName")
    species    = fetch_lookup_map(cursor, "Species",        "SpeciesName")
    alignments = fetch_lookup_map(cursor, "Alignment",      "AlignmentName")
    item_types = fetch_lookup_map(cursor, "ItemType",       "TypeName")
    rarities   = fetch_lookup_map(cursor, "Rarity",         "RarityName")
    regions    = fetch_lookup_map(cursor, "Region",         "RegionName")
    difficulties = fetch_lookup_map(cursor, "Difficulty",   "DifficultyName")

    # ── Characters ────────────────────────────────────────────────────────────
    character_rows = [
        {"CharacterName": "Thorin Ironblade",
            "ClassID": classes["Warrior"]["ClassID"],
            "SpeciesID": species["Dwarf"]["SpeciesID"],
            "AlignmentID": alignments["Lawful Good"]["AlignmentID"],
            "Level": 12
        },
        {"CharacterName": "Lyra Swiftwind",
            "ClassID": classes["Rogue"]["ClassID"],
            "SpeciesID": species["Elf"]["SpeciesID"],
            "AlignmentID": alignments["Chaotic Good"]["AlignmentID"],
            "Level": 8
        },

        {"CharacterName": "Brom Earthshaker",
            "ClassID": classes["Berserker"]["ClassID"],
            "SpeciesID": species["Orc"]["SpeciesID"],
            "AlignmentID": alignments["Chaotic Neutral"]["AlignmentID"],
            "Level": 10
        },

        {"CharacterName": "Seraphina Dawnspear",
            "ClassID": classes["Paladin"]["ClassID"],
            "SpeciesID": species["Human"]["SpeciesID"],
            "AlignmentID": alignments["Lawful Good"]["AlignmentID"],
            "Level": 15
        },

        {"CharacterName": "Morthos the Pale",
            "ClassID": classes["Necromancer"]["ClassID"],
            "SpeciesID": species["Dragonborn"]["SpeciesID"],
            "AlignmentID": alignments["Lawful Evil"]["AlignmentID"],
            "Level": 14
        },

        {"CharacterName": "Pip Underbough",
            "ClassID": classes["Ranger"]["ClassID"],
            "SpeciesID": species["Halfling"]["SpeciesID"],
            "AlignmentID": alignments["Neutral"]["AlignmentID"],
            "Level": 6
        }
    ]

    for row in character_rows:
        cursor.execute("""
            INSERT INTO Character (CharacterName, ClassID, SpeciesID, AlignmentID, Level)
            VALUES (?, ?, ?, ?, ?)
        """, (row["CharacterName"], row["ClassID"], row["SpeciesID"], row["AlignmentID"], row["Level"]))

    print("  ✔ Seeded Character")
    character_map = fetch_lookup_map(cursor, "Character", "CharacterName")

    # ── Items ─────────────────────────────────────────────────────────────────
    item_rows = [
        {"ItemName": "Iron Sword",
          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],
          "RarityID": rarities["Common"]["RarityID"]
        },

        {"ItemName": "Elven Longbow",
           "ItemTypeID": item_types["Weapon"]["ItemTypeID"],
           "RarityID": rarities["Rare"]["RarityID"]
        },

        {"ItemName": "Potion of Healing",
           "ItemTypeID": item_types["Potion"]["ItemTypeID"],
           "RarityID": rarities["Common"]["RarityID"]
        },

        {"ItemName": "Shadowcloak Armor",
           "ItemTypeID": item_types["Armor"]["ItemTypeID"],
           "RarityID": rarities["Epic"]["RarityID"]
        },

        {"ItemName": "Scroll of Firestorm",
           "ItemTypeID": item_types["Scroll"]["ItemTypeID"],
           "RarityID": rarities["Legendary"]["RarityID"]
        },

        {"ItemName": "Amulet of the Ancients",
           "ItemTypeID": item_types["Artifact"]["ItemTypeID"],
           "RarityID": rarities["Legendary"]["RarityID"]
        }
    ]
    for row in item_rows:
        cursor.execute("""
            INSERT INTO Item (ItemName, ItemTypeID, RarityID)
            VALUES (?, ?, ?)
        """, (row["ItemName"], row["ItemTypeID"], row["RarityID"]))

    print("  ✔ Seeded Item")
    item_map = fetch_lookup_map(cursor, "Item", "ItemName")

    # ── Quests ────────────────────────────────────────────────────────────────
    quest_rows = [
        {"QuestName": "Defend the Vale",
           "RegionID": regions["The Verdant Vale"]["RegionID"],
           "DifficultyID": difficulties["Journeyman"]["DifficultyID"]
        },
        {"QuestName": "Shadows Over the Marsh",
           "RegionID": regions["Shadowfen Marshes"]["RegionID"],
           "DifficultyID": difficulties["Expert"]["DifficultyID"]
        },
        {"QuestName": "Climb the Ashpeak",
            "RegionID": regions["Ashpeak Mountains"]["RegionID"],
            "DifficultyID": difficulties["Master"]["DifficultyID"]
        },
        {"QuestName": "Whispers in the Trees",
            "RegionID": regions["Whispering Woods"]["RegionID"],
            "DifficultyID": difficulties["Novice"]["DifficultyID"]
        },
        {"QuestName": "Stormbreak Siege",
            "RegionID": regions["Stormbreak Coast"]["RegionID"],
            "DifficultyID": difficulties["Legendary"]["DifficultyID"]
        },
        {"QuestName": "The Necromancer’s Bargain",
            "RegionID": regions["Shadowfen Marshes"]["RegionID"],
            "DifficultyID": difficulties["Expert"]["DifficultyID"]
        }
]

    for row in quest_rows:
        cursor.execute("""
            INSERT INTO Quest (QuestName, RegionID, DifficultyID)
            VALUES (?, ?, ?)
        """, (row["QuestName"], row["RegionID"], row["DifficultyID"]))

    print("  ✔ Seeded Quest")
    quest_map = fetch_lookup_map(cursor, "Quest", "QuestName")

    # ── Inventory ─────────────────────────────────────────────────────────────
    inventory_rows = [
        {"CharacterID": character_map["Thorin Ironblade"]["CharacterID"],    "ItemID": item_map["Iron Sword"]["ItemID"],           "Quantity": 1},
    ]

    for row in inventory_rows:
        cursor.execute("""
            INSERT INTO Inventory (CharacterID, ItemID, Quantity)
            VALUES (?, ?, ?)
        """, (row["CharacterID"], row["ItemID"], row["Quantity"]))

    print("  ✔ Seeded Inventory")

    # ── CharacterQuest ────────────────────────────────────────────────────────
    character_quest_rows = [
    {
        "CharacterID": character_map["Thorin Ironblade"]["CharacterID"],
        "QuestID": quest_map["Defend the Vale"]["QuestID"],
        "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")
    },
    {
        "CharacterID": character_map["Lyra Swiftwind"]["CharacterID"],
        "QuestID": quest_map["Shadows Over the Marsh"]["QuestID"],
        "CompletionDate": datetime(2026, 2, 5, 10, 15).isoformat(sep=" ")
    },
    {
        "CharacterID": character_map["Brom Earthshaker"]["CharacterID"],
        "QuestID": quest_map["Climb the Ashpeak"]["QuestID"],
        "CompletionDate": datetime(2026, 3, 18, 16, 45).isoformat(sep=" ")
    },
    {
        "CharacterID": character_map["Seraphina Dawnspear"]["CharacterID"],
        "QuestID": quest_map["Whispers in the Trees"]["QuestID"],
        "CompletionDate": datetime(2026, 4, 2, 9, 20).isoformat(sep=" ")
    },
    {
        "CharacterID": character_map["Morthos the Pale"]["CharacterID"],
        "QuestID": quest_map["Stormbreak Siege"]["QuestID"],
        "CompletionDate": datetime(2026, 5, 11, 18, 5).isoformat(sep=" ")
    },
    {
        "CharacterID": character_map["Pip Underbough"]["CharacterID"],
        "QuestID": quest_map["The Necromancer’s Bargain"]["QuestID"],
        "CompletionDate": datetime(2026, 6, 7, 12, 0).isoformat(sep=" ")
    }
]

    

      
    

    for row in character_quest_rows:
        cursor.execute("""
            INSERT INTO CharacterQuest (CharacterID, QuestID, CompletionDate)
            VALUES (?, ?, ?)
        """, (row["CharacterID"], row["QuestID"], row["CompletionDate"]))

    print("  ✔ Seeded CharacterQuest")


def seed():
    init_db()
    conn = get_db()          # was: get_connection() - does not exist
    cursor = conn.cursor()

    try:
        seed_lookup_tables(cursor)
        seed_core_data(cursor)
        conn.commit()
        print("\nSeed complete.")
    except Exception as e:
        conn.rollback()
        print(f"\nSeed failed: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    seed()