import requests
from rich.progress import track

CHARS_PER_SITE = 10000

bad = []
with open("bad", "r", encoding="utf-8") as f:
    for line in f:
        bad.append("http://" + line.strip())

for u in track(bad):
    print(u)
    try:
        r = requests.get(u)
    except Exception:
        continue
    if len(r.text) > CHARS_PER_SITE:
        print(r.text[:CHARS_PER_SITE])
    else:
        print(r.text)
