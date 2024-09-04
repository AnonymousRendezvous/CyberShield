from os import remove
from os.path import exists

import requests
from rich.progress import track

CHARS_PER_SITE = 10000

bad = []
with open("good", "r", encoding="utf-8") as f:
    for line in f:
        bad.append("http://" + line.strip())

if exists("good.out"):
    remove("good.out")
with open("good.out", "a", encoding="utf-8") as f:
    for u in track(bad):
        print(u)
        try:
            r = requests.get(u, timeout=5)
        except Exception:
            continue
        if len(r.text) > CHARS_PER_SITE:
            html = r.text[:CHARS_PER_SITE]
        else:
            html = r.text
        html = html.replace("\n", " ").replace(",", " ")
        f.write(u + " " + html + "\n")
