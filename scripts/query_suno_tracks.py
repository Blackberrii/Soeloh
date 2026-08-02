"""
Pulls the public track catalog for @generatedbyaccident from suno.com and
writes tracks.json at the repo root, so the static site can render a live
list instead of hardcoded placeholder titles.

This is NOT an official Suno API — Suno doesn't have one for profile data.
The profile page is a Next.js app that embeds the full catalog as JSON
inside its React Server Component payload (the `self.__next_f.push(...)`
script chunks). This script decodes those chunks and pulls clip objects
out with a brace-matching scan, since the payload as a whole isn't valid
JSON (it's React Flight wire format, not a plain JSON document).

Fragile by nature: if Suno changes their frontend structure, this can
silently stop finding clips. On any failure or a zero-clip result, the
script exits without touching tracks.json, so the site keeps showing the
last known-good catalog instead of going blank. Run on a schedule by
.github/workflows/suno-tracks.yml.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

PROFILE_URL = "https://suno.com/@generatedbyaccident"
MAX_TRACKS = 20
MAX_TAGS_PER_TRACK = 4
TIMEOUT = 15
FETCH_ATTEMPTS = 3
OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tracks.json")

NEXT_F_CHUNK_RE = re.compile(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', re.S)
CLIP_START_RE = re.compile(r'"content_type":"clip","content_item":(\{)')
CLIPS_COUNT_RE = re.compile(r'"clips_count":(\d+)')


def fetch_profile_html():
    req = urllib.request.Request(
        PROFILE_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    last_exc = None
    for attempt in range(FETCH_ATTEMPTS):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            last_exc = exc
            if attempt < FETCH_ATTEMPTS - 1:
                time.sleep(2 * (attempt + 1))
    raise last_exc


def decode_rsc_payload(html):
    chunks = NEXT_F_CHUNK_RE.findall(html)
    parts = []
    for c in chunks:
        try:
            decoded = json.loads(c)
        except Exception:
            continue
        if isinstance(decoded, str):
            parts.append(decoded)
    return "\n".join(parts)


def extract_json_object(s, start):
    """s[start] must be '{'. Returns the balanced substring for that object."""
    depth = 0
    i = start
    in_str = False
    esc = False
    while i < len(s):
        c = s[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return s[start : i + 1]
        i += 1
    return None


def extract_clips(payload):
    clips = []
    seen = set()
    for m in CLIP_START_RE.finditer(payload):
        obj_str = extract_json_object(payload, m.start(1))
        if not obj_str:
            continue
        try:
            obj = json.loads(obj_str)
        except Exception:
            continue
        clip_id = obj.get("id")
        if not clip_id or clip_id in seen:
            continue
        if not obj.get("is_public", True) or obj.get("status") != "complete":
            continue
        seen.add(clip_id)
        clips.append(obj)
    return clips


def clean_title(title):
    title = re.sub(r"\s+", " ", (title or "").strip())
    if title and (title.isupper() or title.islower()):
        title = title.title()
    if len(title) > 70:
        title = title[:69].rstrip() + "…"
    return title or "Untitled"


def clean_tags(clip):
    raw = clip.get("display_tags") or clip.get("metadata", {}).get("tags") or ""
    tags = []
    for t in raw.split(","):
        t = t.strip().lower()
        if not t:
            continue
        if len(t) > 28:
            t = t[:27].rstrip() + "…"
        tags.append(t)
    return tags[:MAX_TAGS_PER_TRACK]


def build_track(clip):
    return {
        "id": clip["id"],
        "title": clean_title(clip.get("title")),
        "tags": clean_tags(clip),
        "audio_url": clip.get("audio_url"),
        "url": f"https://suno.com/song/{clip['id']}",
        "play_count": clip.get("play_count", 0),
        "created_at": clip.get("created_at"),
    }


def main():
    html = fetch_profile_html()
    payload = decode_rsc_payload(html)
    clips = extract_clips(payload)

    if not clips:
        print("no clips found — leaving tracks.json untouched", file=sys.stderr)
        return 1

    clips.sort(key=lambda c: c.get("created_at") or "", reverse=True)
    tracks = [build_track(c) for c in clips[:MAX_TRACKS]]

    count_match = CLIPS_COUNT_RE.search(payload)
    total_public_clips = int(count_match.group(1)) if count_match else len(clips)

    result = {
        "tracks": tracks,
        "total_public_clips": total_public_clips,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    print(f"wrote {len(tracks)} tracks (of {total_public_clips} public clips)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"error — leaving tracks.json untouched: {exc}", file=sys.stderr)
        sys.exit(1)
