#!/usr/bin/env python3
"""
log_sighting.py — Log a bird sighting to lifeList.json.

Usage:
  python log_sighting.py \
    --species "American Robin" \
    --scientific-name "Turdus migratorius" \
    --rarity "common" \
    --region "California" \
    [--notes "Spotted in backyard"] \
    [--workspace "./birdfolio"]

Output (JSON to stdout):
  {"status": "ok", "sighting": {...}, "isLifer": true, "totalSightings": 1, "totalSpecies": 1}
"""
import argparse
import json
import os
from datetime import datetime, timezone


def slugify(name):
    return name.lower().replace(" ", "-").replace("'", "").replace(".", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--species", required=True, help="Common name (e.g. 'American Robin')")
    parser.add_argument("--scientific-name", required=True, help="Scientific name")
    parser.add_argument("--rarity", required=True, choices=["common", "rare", "superRare", "bonus"])
    parser.add_argument("--region", required=True, help="Region where spotted")
    parser.add_argument("--notes", default="", help="Optional observer notes")
    parser.add_argument("--workspace", default="./birdfolio", help="Workspace directory")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    life_list_path = os.path.join(workspace, "lifeList.json")
    config_path = os.path.join(workspace, "config.json")

    # Load existing data
    life_list = []
    if os.path.exists(life_list_path):
        with open(life_list_path) as f:
            life_list = json.load(f)

    config = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)

    slug = slugify(args.species)

    # Duplicate detection — already in life list?
    seen_slugs = {entry.get("slug") for entry in life_list}
    is_lifer = slug not in seen_slugs

    if not is_lifer:
        print(json.dumps({
            "status": "duplicate",
            "message": f"{args.species} is already in your life list — not logging again.",
            "slug": slug
        }))
        return

    sighting = {
        "id": f"sighting-{len(life_list) + 1:03d}",
        "commonName": args.species,
        "scientificName": args.scientific_name,
        "slug": slug,
        "rarity": args.rarity,
        "region": args.region,
        "date": datetime.now(timezone.utc).isoformat(),
        "isLifer": is_lifer,
        "notes": args.notes,
        "cardSent": False
    }

    life_list.append(sighting)

    with open(life_list_path, "w") as f:
        json.dump(life_list, f, indent=2)

    # Update config counters
    config["totalSightings"] = config.get("totalSightings", 0) + 1
    if is_lifer:
        config["totalSpecies"] = config.get("totalSpecies", 0) + 1

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(json.dumps({
        "status": "ok",
        "sighting": sighting,
        "isLifer": is_lifer,
        "totalSightings": config["totalSightings"],
        "totalSpecies": config["totalSpecies"]
    }))


if __name__ == "__main__":
    main()
