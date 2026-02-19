#!/usr/bin/env python3
"""
upload_card.py — Upload a card PNG via the Birdfolio API (no R2 credentials needed).

Usage:
  python upload_card.py <png_path> [--api-url <url>] [--workspace <path>]

Output (JSON to stdout):
  {"status": "ok", "url": "https://pub-xxx.r2.dev/cards/filename.png"}
"""
import sys, os, json, argparse, urllib.request, urllib.error

def load_config(workspace):
    cfg_path = os.path.join(workspace, "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            return json.load(f)
    return {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("png_path")
    parser.add_argument("--api-url", default=None)
    parser.add_argument("--workspace", default=None)
    args = parser.parse_args()

    png_path = os.path.abspath(args.png_path)
    if not os.path.exists(png_path):
        print(json.dumps({"status": "error", "message": f"File not found: {png_path}"}))
        sys.exit(1)

    # Resolve workspace + config
    workspace = args.workspace
    if not workspace:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace = os.path.abspath(os.path.join(script_dir, "..", "..", "..", "birdfolio"))

    cfg = load_config(workspace)
    api_url = (args.api_url or cfg.get("apiUrl", "https://birdfolio.tonbistudio.com")).rstrip("/")

    filename = os.path.basename(png_path)
    boundary = "----BirdfolioUpload"

    with open(png_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"{api_url}/cards/upload",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )

    try:
        res = urllib.request.urlopen(req, timeout=30)
        result = json.loads(res.read().decode())
        print(json.dumps({"status": "ok", "url": result["url"]}))
    except urllib.error.HTTPError as e:
        body_err = e.read().decode()
        print(json.dumps({"status": "error", "code": e.code, "message": body_err}))
        sys.exit(1)

if __name__ == "__main__":
    main()
