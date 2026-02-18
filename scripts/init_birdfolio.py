#!/usr/bin/env python3
"""
init_birdfolio.py — Create Birdfolio workspace structure.

Creates folders and empty JSON stubs. The agent populates checklist.json
with species data (from You.com search results) using write_file after this runs.

Usage:
  python init_birdfolio.py --region "California" [--workspace "./birdfolio"]

Output (JSON to stdout):
  {"status": "ok", "workspace": "...", "region": "...", "created": [...], "next": "..."}
"""
import argparse
import json
import os
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True, help="Home region (e.g. 'California')")
    parser.add_argument("--workspace", default="./birdfolio", help="Workspace directory")
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    region = args.region.strip()
    created = []

    # Create directory structure
    for subdir in ["", "birds", "cards"]:
        path = os.path.join(workspace, subdir)
        os.makedirs(path, exist_ok=True)
        if subdir:
            created.append(path)

    # config.json
    config_path = os.path.join(workspace, "config.json")
    if not os.path.exists(config_path):
        config = {
            "version": 1,
            "setupDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "homeRegion": region,
            "regions": [region],
            "totalSightings": 0,
            "totalSpecies": 0
        }
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        created.append("config.json")

    # lifeList.json
    life_list_path = os.path.join(workspace, "lifeList.json")
    if not os.path.exists(life_list_path):
        with open(life_list_path, "w") as f:
            json.dump([], f, indent=2)
        created.append("lifeList.json")

    # checklist.json — empty structure; agent writes species data via write_file
    checklist_path = os.path.join(workspace, "checklist.json")
    if not os.path.exists(checklist_path):
        checklist = {
            region: {
                "common": [],
                "rare": [],
                "superRare": []
            }
        }
        with open(checklist_path, "w") as f:
            json.dump(checklist, f, indent=2)
        created.append("checklist.json")

    print(json.dumps({
        "status": "ok",
        "workspace": workspace,
        "region": region,
        "files_created": created,
        "checklist_path": checklist_path,
        "next": (
            f"Workspace ready. Now use write_file to populate {checklist_path} "
            f"with species from You.com search results (10 common, 5 rare, 1 superRare). "
            f"See references/data-schema.md for the checklist.json format."
        )
    }))


if __name__ == "__main__":
    main()
