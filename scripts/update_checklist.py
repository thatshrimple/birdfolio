#!/usr/bin/env python3
"""
update_checklist.py — Mark a species as found on the regional checklist.

Searches all rarity tiers (common, rare, superRare) for the species.
If found, marks it with today's date. Safe to run even if species isn't on checklist.

Usage:
  python update_checklist.py \
    --species "American Robin" \
    --region "California" \
    [--date "2026-02-20"] \
    [--workspace "./birdfolio"]

Output (JSON to stdout):
  {"status": "ok"|"not_on_checklist", "species": "...", "tier": "...", "dateFound": "..."}
"""
import argparse
import json
import os
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--species", required=True, help="Common name of the species")
    parser.add_argument("--region", required=True, help="Region")
    parser.add_argument("--date", default=None, help="Date found YYYY-MM-DD, defaults to today")
    parser.add_argument("--workspace", default="./birdfolio", help="Workspace directory")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    checklist_path = os.path.join(workspace, "checklist.json")

    if not os.path.exists(checklist_path):
        print(json.dumps({"status": "error", "message": "checklist.json not found — run init_birdfolio.py first"}))
        return

    with open(checklist_path) as f:
        checklist = json.load(f)

    region_data = checklist.get(args.region, {})
    date_found = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    species_lower = args.species.lower()

    found_tier = None
    already_found = False

    for tier in ("common", "rare", "superRare"):
        for entry in region_data.get(tier, []):
            if entry.get("species", "").lower() == species_lower:
                if entry.get("found"):
                    already_found = True
                else:
                    entry["found"] = True
                    entry["dateFound"] = date_found
                found_tier = tier
                break
        if found_tier:
            break

    if found_tier:
        if not already_found:
            with open(checklist_path, "w") as f:
                json.dump(checklist, f, indent=2)

        print(json.dumps({
            "status": "ok",
            "species": args.species,
            "region": args.region,
            "tier": found_tier,
            "dateFound": date_found,
            "alreadyFound": already_found
        }))
    else:
        print(json.dumps({
            "status": "not_on_checklist",
            "message": f"{args.species} is not on the {args.region} checklist — sighting still logged to life list"
        }))


if __name__ == "__main__":
    main()
