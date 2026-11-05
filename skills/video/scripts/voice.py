#!/usr/bin/env python3
"""Generate ElevenLabs takes with per-character timestamps.

    python3 voice.py SCRIPT.txt --voice-id <id> --takes 2 --out voice/
    python3 voice.py voice/ch1.txt voice/ch4.txt --voice-id <id>      # only the chapters that changed

Writes <out>/<name>-take<i>.mp3 and <name>-take<i>-alignment.json for each text file.
The API key is read from $ELEVENLABS_API_KEY, else from the macOS keychain (service "elevenlabs").
It is never printed or written anywhere.
"""
import argparse, base64, json, os, pathlib, subprocess, sys, urllib.error, urllib.request

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_192"


def api_key(service):
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if key:
        return key
    try:
        return subprocess.run(["security", "find-generic-password", "-s", service, "-w"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        sys.exit(f"No API key: set ELEVENLABS_API_KEY or add a keychain item (service '{service}').")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("texts", nargs="+", type=pathlib.Path, help="text files, tone tags like [excited] allowed")
    p.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID"), help="or $ELEVENLABS_VOICE_ID")
    p.add_argument("--model", default="eleven_v4")
    p.add_argument("--stability", type=float, default=0.38)
    p.add_argument("--similarity", type=float, default=0.85)
    p.add_argument("--lang", default="fr", help="language_code sent to the API")
    p.add_argument("--takes", type=int, default=2)
    p.add_argument("--previous", default=None, help="previous_text, to keep the intonation of an inserted sentence")
    p.add_argument("--next", default=None, help="next_text, same purpose")
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("voice"))
    p.add_argument("--keychain-service", default="elevenlabs")
    a = p.parse_args()
    if not a.voice_id:
        p.error("--voice-id (or $ELEVENLABS_VOICE_ID) is required")
    key = api_key(a.keychain_service)
    a.out.mkdir(parents=True, exist_ok=True)
    failed = 0
    for text_file in a.texts:
        body = {"text": text_file.read_text(encoding="utf-8").strip(), "model_id": a.model, "language_code": a.lang,
                "voice_settings": {"stability": a.stability, "similarity_boost": a.similarity}}
        if a.previous:
            body["previous_text"] = a.previous
        if a.next:
            body["next_text"] = a.next
        for i in range(1, a.takes + 1):
            stem = a.out / f"{text_file.stem}-take{i}"
            for attempt in range(1, 4):
                req = urllib.request.Request(API.format(voice=a.voice_id), data=json.dumps(body).encode(),
                                             headers={"xi-api-key": key, "Content-Type": "application/json"})
                try:
                    with urllib.request.urlopen(req, timeout=600) as r:
                        data = json.load(r)
                    stem.with_suffix(".mp3").write_bytes(base64.b64decode(data["audio_base64"]))
                    pathlib.Path(f"{stem}-alignment.json").write_text(json.dumps(data["alignment"], ensure_ascii=False))
                    print(f"{stem}.mp3 ok")
                    break
                except urllib.error.HTTPError as e:
                    print(f"{stem.name} attempt {attempt}: HTTP {e.code} {e.read()[:200]!r}")
                except Exception as e:  # network errors: retry
                    print(f"{stem.name} attempt {attempt}: {e}")
            else:
                failed += 1
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
