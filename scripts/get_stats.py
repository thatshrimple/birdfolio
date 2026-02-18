#!/usr/bin/env python3
"""
get_stats.py — Return life list stats and checklist progress.

Usage:
  python get_stats.py [--workspace "./birdfolio"]

Output (JSON to stdout): full stats object for the agent to format.
"""
import argparse
import json
import os


TIER_RANK = {"superRare": 3, "rare": 2, "common": 1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default="./birdfolio", help="Workspace directory")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)

    # Load files
    config = {}
    config_path = os.path.join(workspace, "config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)

    checklist = {}
    checklist_path = os.path.join(workspace, "checklist.json")
    if os.path.exists(checklist_path):
        with open(checklist_path) as f:
            checklist = json.load(f)

    life_list = []
    life_list_path = os.path.join(workspace, "lifeList.json")
    if os.path.exists(life_list_path):
        with open(life_list_path) as f:
            life_list = json.load(f)

    # Checklist progress per region
    checklist_progress = {}
    for region, tiers in checklist.items():
        checklist_progress[region] = {}
        for tier in ("common", "rare", "superRare"):
            entries = tiers.get(tier, [])
            found_entries = [e for e in entries if e.get("found")]
            checklist_progress[region][tier] = {
                "found": len(found_entries),
                "total": len(entries),
                "species": entries
            }

    # Rarity breakdown from life list (lifers only, for unique species count)
    rarity_counts = {"common": 0, "rare": 0, "superRare": 0}
    lifers = [e for e in life_list if e.get("isLifer")]
    for entry in lifers:
        r = entry.get("rarity", "common")
        rarity_counts[r] = rarity_counts.get(r, 0) + 1

    # Most recent sighting
    most_recent = life_list[-1] if life_list else None

    # Rarest lifer
    rarest = (
        max(lifers, key=lambda e: TIER_RANK.get(e.get("rarity", "common"), 0))
        if lifers else None
    )

    total_sightings = config.get("totalSightings", len(life_list))
    total_species = config.get("totalSpecies", len({e.get("slug") for e in life_list}))

    print(json.dumps({
        "status": "ok",
        "homeRegion": config.get("homeRegion", ""),
        "setupDate": config.get("setupDate", ""),
        "totalSightings": total_sightings,
        "totalSpecies": total_species,
        "rarityBreakdown": rarity_counts,
        "checklistProgress": checklist_progress,
        "mostRecentSighting": most_recent,
        "rarestBird": rarest
    }))


if __name__ == "__main__":
    main()
