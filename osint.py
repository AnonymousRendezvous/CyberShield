import tkinter as tk
from tkinter import simpledialog
# pip install duckduckgo_search
from duckduckgo_search import DDGS
# pip install -U g4f
from g4f.client import Client
from g4f.Provider import Ecosia
import requests, json
import sys
import os

class OSINT(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Query:").grid(row=0)
        tk.Label(master, text="Any other information:").grid(row=1)
        tk.Label(master, text="Do you want to trawl for images? (beta testing) y/n: ").grid(row=2)
        tk.Label(master, text="Input your email address: ").grid(row=3)

        self.e0 = tk.Entry(master)
        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)

    def apply(self):
        self.result = (
            self.e0.get(),
            self.e1.get(),
            self.e2.get(),
            self.e3.get(),
        )

# global variables
finalpayload = ""
storenum = 0
storemsg = ""
storemsg = ""

def payload_gen(word, add, img):
    new = '"' + word + '"'

    if img == "y":
        results = DDGS().text(new, max_results=25)
        images = DDGS().images(new, region="sg-en", max_results=25)
    else:
        results = DDGS().text(new, max_results=50)
        print(results)
    global finalpayload
    payload = f"If I gave you some information on someone, could you write me a comprehensive report on them that is as detailed as possible?"
    payload += f" Do note that the person's name is, {word}. Perhaps you could also create a web of people relating to {word} and provide ANY and ALL links where the information can be found."
    payload += "Do also see if you can extract basic information such as past and current education statuses, location and information from ANY accounts like their username or email."
    payload += f"Lastly, also note that {add}  Here is the data with links (to be included): \n."
    gptstring = ""
    refgptstr = ""
    if img == "y":
        for x in results:
            gptstring += ' '
            gptstring += str(x)

        for x in images:
            refgptstr += ' '
            refgptstr += str(x)

        payload += " Data: " + gptstring
        payloadimg = f" Now, with the above data, I will provide you with some image links relating to {word}."
        payloadimg += f" Do filter through all the data and give me ANY relevant links. Here is the data: {refgptstr}."
        finalpayload += payload + " " + payloadimg
    else:   
        for x in results:
            gptstring += ' '
            gptstring += str(x)

        payload += " Data: " + gptstring
        finalpayload += payload

def chat(finalpayload, storemsg):
    client = Client(provider=Ecosia)
    storemsg = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": finalpayload}]
    )
    print(storemsg.choices[0].message.content) 

def email_address(email):
  url = "https://webapi.namescan.io/v1/freechecks/email/breaches"

  payload={
      "email": email
  }
  headers = {
      'Content-Type': 'application/json'
  }
  response = requests.post(url, headers=headers, data=json.dumps(payload))
  print(response.text)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    d = OSINT(root)
    if d.result:  # Check if the dialog returned a result
        word, add, img, email = d.result
        # Runs the function in a separate thread
        payload_gen(word, add, img)
        chat(finalpayload, storemsg)
        email_address(email)
    else: 
        print("failed")

main()

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt 4 api
