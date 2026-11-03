"""Builds the legal pages from the Markdown in this folder.

Run from anywhere:  python src/build.py
Edit privacy.md / terms.md, change UPDATED below, rebuild, commit and push.
"""
import re
from pathlib import Path

import markdown

UPDATED = "3 November 2026"

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent

PAGES = [
    ("privacy.md", "privacy.html", "Privacy Policy"),
    ("terms.md", "terms.html", "Terms of Use"),
]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · BallerZ</title>
<meta name="description" content="{title} for BallerZ, a free online football game by nuuunu Games.">
<link rel="icon" href="logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Saira+Semi+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="bar">
  <a class="logo" href="./"><img src="logo.png" alt="BallerZ"></a>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p>nuuunu Games · <a href="mailto:nuuunugames@gmail.com">nuuunugames@gmail.com</a></p>
</footer>
</body>
</html>
"""


def nav(current):
    links = []
    for _, html, title in PAGES:
        cls = ' class="on"' if html == current else ""
        links.append(f'<a href="{html}"{cls}>{title}</a>')
    return "".join(links)


def build_page(md_name, html_name, title):
    text = (SRC / md_name).read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["tables", "toc"])
    body = md.convert(text)
    # The date line goes right under the page title.
    body = re.sub(r"(</h1>)", rf'\1\n<p class="updated">Last updated: {UPDATED}</p>', body, count=1)
    # Wide tables scroll sideways on phones instead of the whole page.
    body = body.replace("<table>", '<div class="table"><table>').replace("</table>", "</table></div>")
    page = TEMPLATE.format(title=title, nav=nav(html_name), body=body)
    (ROOT / html_name).write_text(page, encoding="utf-8", newline="\n")


def build_index():
    cards = "".join(
        f'<a class="card" href="{html}"><span>{title}</span><span class="go">Read &rarr;</span></a>'
        for _, html, title in PAGES)
    body = ('<h1>BallerZ legal</h1>\n<p class="updated">Last updated: ' + UPDATED + '</p>\n'
            '<p>BallerZ is a free online football game by nuuunu Games. '
            'These pages explain the rules of the game\'s community and how your data is handled.</p>\n'
            f'<div class="cards">{cards}</div>')
    page = TEMPLATE.format(title="Legal", nav=nav("index.html"), body=body)
    (ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    for page in PAGES:
        build_page(*page)
    build_index()
    print("Built", ", ".join(h for _, h, _ in PAGES), "and index.html")
