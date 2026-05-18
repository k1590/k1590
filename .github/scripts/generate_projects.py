import urllib.request
import json
import os
import re

USERNAME = "k1590"
EXCLUDE_REPOS = {"k1590", "k1590.github.io", "github-profile"}
README_PATH = "README.md"

START_MARKER = "<!-- START_PROJECTS -->"
END_MARKER = "<!-- END_PROJECTS -->"


def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?type=public&sort=updated&per_page=100&direction=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "k1590-readme-bot"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def format_table(repos):
    rows = ["| Project | Description | Language |", "|---------|-------------|----------|"]
    for r in repos:
        name = r["name"]
        desc = (r["description"] or "No description")[:80]
        lang = r["language"] or "—"
        url = r["html_url"]
        rows.append(f"| [{name}]({url}) | {desc} | {lang} |")
    return "\n".join(rows) if len(rows) > 2 else "_No public repositories found._"


def main():
    all_repos = fetch_repos()

    repos = [
        r for r in all_repos
        if r["name"] not in EXCLUDE_REPOS and r["fork"] is False
    ]

    table = format_table(repos)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        START_MARKER + "\n" + table + "\n" + END_MARKER,
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
