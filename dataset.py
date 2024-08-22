from random import choice

with open("hosts", "r", encoding="utf-8") as f:
    e = list(f)
    for i in range(2000):
        print(choice(e).strip()[8:])
