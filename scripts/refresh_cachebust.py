#!/usr/bin/env python3
"""
refresh_cachebust.py

Appends/updates a `&cb=<timestamp>` query param on the github-readme-stats
and github-readme-streak-stats image URLs in README.md. Changing the image
URL every run forces GitHub's camo CDN to fetch a fresh copy instead of
serving a stale cached snapshot.

Run manually:
    python3 scripts/refresh_cachebust.py

Or let the GitHub Action (.github/workflows/refresh-stats.yml) run it on
a daily schedule.
"""

import os
import re
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, "README.md")

# Matches any github-readme-stats / streak-stats image URL inside README.md
URL_RE = re.compile(
    r'(https://(?:github-readme-stats\.vercel\.app|github-readme-streak-stats\.herokuapp\.com)[^\s"\'>]*)'
)


def bust(url, timestamp):
    # Strip any existing cb= param, then append a fresh one
    url = re.sub(r"[&?]cb=\d+", "", url)
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}cb={timestamp}"


def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    timestamp = int(datetime.now(timezone.utc).timestamp())
    new_content = URL_RE.sub(lambda m: bust(m.group(1), timestamp), content)

    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated with fresh cache-busting params.")
    else:
        print("No matching stat URLs found or nothing to change.")


if __name__ == "__main__":
    main()
