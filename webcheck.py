import requests, json
# pip install beautifulsoup4
from bs4 import BeautifulSoup

website = input("Website: ")

def linkchecker(website):
    url = website
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        print(link.get('href'))

def authentication(website):
    auth = str(website)
    for x in auth:
        if x == "affiliate":
            print("hi")

linkchecker(website)
