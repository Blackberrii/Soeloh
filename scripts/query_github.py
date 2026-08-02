"""
Pulls live GitHub data for the Active Projects section: public repos (with
per-repo language breakdown + topics) and the last 5 public events. Writes
github.json at the repo root; the site fetches that same-origin instead of
calling the GitHub API directly from every visitor's browser.

Why not just call the GitHub API client-side (which is what this replaced)?
It works, but it means every page load depends on GitHub's API being up and
fast at that exact moment, and the richer per-repo data (language %, topics)
needs extra calls per repo that aren't worth making on every single page view.
Doing it here on a schedule means one set of calls per run instead of one set
per visitor, and the site can show it instantly from a local file.

Fails safe like the other query scripts: on any error, or if the GitHub API
returns nothing usable, this leaves github.json untouched rather than wiping
the site's copy — a bad run just means slightly stale data, not an empty
section. Run on a schedule by .github/workflows/github-data.yml.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

USERNAME = "Blackberrii"
EXCLUDE_REPOS = {"soeloh"}  # lowercase repo names to skip (the site's own repo)
MAX_PROJECTS = 6
MAX_ACTIVITY = 5
TIMEOUT = 15
OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "github.json")

API = "https://api.github.com"


def api_get(path):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USERNAME}-site-script",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def language_breakdown(owner_repo):
    try:
        bytes_by_lang = api_get(f"/repos/{owner_repo}/languages")
    except Exception:
        return []
    total = sum(bytes_by_lang.values())
    if not total:
        return []
    ranked = sorted(bytes_by_lang.items(), key=lambda kv: kv[1], reverse=True)
    return [
        {"name": name, "percent": round(n / total * 100, 1)}
        for name, n in ranked[:4]
    ]


def build_projects():
    repos = api_get(f"/users/{USERNAME}/repos?type=public&sort=pushed&per_page=100")
    if not isinstance(repos, list):
        raise ValueError("unexpected /repos response")

    repos = [
        r for r in repos
        if not r.get("fork") and not r.get("archived") and r["name"].lower() not in EXCLUDE_REPOS
    ]
    repos.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)

    projects = []
    for r in repos[:MAX_PROJECTS]:
        projects.append({
            "name": r["name"],
            "description": r.get("description"),
            "url": r["html_url"],
            "languages": language_breakdown(r["full_name"]),
            "topics": (r.get("topics") or [])[:3],
            "stars": r.get("stargazers_count", 0),
            "pushed_at": r.get("pushed_at"),
        })
    return projects


def describe_event(ev):
    repo = ev["repo"]["name"].split("/", 1)[1]
    t = ev["type"]
    payload = ev.get("payload", {})

    if t == "PushEvent":
        url = f"https://github.com/{ev['repo']['name']}/commit/{payload.get('head', '')}"
        return f"Pushed to {repo}", url
    if t == "CreateEvent":
        return f"Created {payload.get('ref_type', 'ref')} in {repo}", f"https://github.com/{ev['repo']['name']}"
    if t == "DeleteEvent":
        return f"Deleted {payload.get('ref_type', 'ref')} in {repo}", f"https://github.com/{ev['repo']['name']}"
    if t == "WatchEvent":
        return f"Starred {repo}", f"https://github.com/{ev['repo']['name']}"
    if t == "ForkEvent":
        return f"Forked {repo}", f"https://github.com/{ev['repo']['name']}"
    if t == "PullRequestEvent":
        pr = payload.get("pull_request") or {}
        return f"{payload.get('action', 'updated')} a PR in {repo}", pr.get("html_url", f"https://github.com/{ev['repo']['name']}")
    if t == "IssuesEvent":
        issue = payload.get("issue") or {}
        return f"{payload.get('action', 'updated')} an issue in {repo}", issue.get("html_url", f"https://github.com/{ev['repo']['name']}")
    return f"{t.replace('Event', '')} in {repo}", f"https://github.com/{ev['repo']['name']}"


def commit_message(owner_repo, sha):
    try:
        commit = api_get(f"/repos/{owner_repo}/commits/{sha}")
        msg = commit.get("commit", {}).get("message", "")
        return msg.split("\n")[0] if msg else None
    except Exception:
        return None


def build_activity():
    events = api_get(f"/users/{USERNAME}/events/public?per_page=10")
    if not isinstance(events, list):
        raise ValueError("unexpected /events response")

    activity = []
    for ev in events[:MAX_ACTIVITY]:
        label, url = describe_event(ev)
        if ev["type"] == "PushEvent":
            msg = commit_message(ev["repo"]["name"], ev["payload"].get("head", ""))
            if msg:
                label = msg
        activity.append({
            "label": label,
            "url": url,
            "created_at": ev["created_at"],
        })
    return activity


def main():
    projects = build_projects()
    activity = build_activity()

    if not projects and not activity:
        print("nothing usable came back — leaving github.json untouched", file=sys.stderr)
        return 1

    result = {
        "projects": projects,
        "activity": activity,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    print(f"wrote {len(projects)} projects, {len(activity)} activity items")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"error — leaving github.json untouched: {exc}", file=sys.stderr)
        sys.exit(1)
