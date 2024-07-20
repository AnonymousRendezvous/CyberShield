import tkinter as tk
from tkinter import simpledialog
# pip install duckduckgo_search
from duckduckgo_search import DDGS
# pip install -U g4f
import g4f
from g4f.client import Client
import requests, json
import time

class OSINT(simpledialog.Dialog):

    def body(self, master):
        tk.Label(master, text="Query:").grid(row=0)
        tk.Label(master, text="Any other information:").grid(row=1)
        tk.Label(master, text="Do you want to trawl for images? (beta testing) y/n: ").grid(row=2)
        tk.Label(master, text="Input your email address: ").grid(row=3)
        tk.Label(master, text="Input your instagram username (beta testing): ").grid(row=4)

        self.e0 = tk.Entry(master)
        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)
        self.e4 = tk.Entry(master)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)

    def apply(self):
        self.result = (
            self.e0.get(),
            self.e1.get(),
            self.e2.get(),
            self.e3.get(),
            self.e4.get(),
        )


# global variables
payload = ""
payload2 = ""
payload3 = ""

messages = []

# g4f client provider
client = Client(provider=g4f.Provider.MetaAI)


def payload_gen(word, add, img):
    global payload, payload2, payload3
    new = '"' + word + '"'

    if img == "y":
        #Beta testing for images
        results = DDGS().text(new, max_results=4)
        images = DDGS().images(new, region="sg-en", max_results=1)
    else:
        results = DDGS().text(new, region="sg-en:",max_results=10)
        print("Results found: " + str(len(results)))

    payload = f"Write me a comprehensive report on a person that is as detailed as possible?"
    payload += f" Do note that the person's name is, {word}. Perhaps you could also create a web of people relating to them and provide ANY and ALL links where the information can be found."
    payload += "Do also see if you can extract basic information such as past and current education statuses, location and information from ANY accounts like their username or email."
    payload += f"Lastly, also note that {add}  Here is the data with links (to be included): \n."
    gptstring = ""
    gptstring2 = ""
    refgptstr = ""
    if img == "y":
        for x in results:
            gptstring += ' '
            gptstring += str(x)

        for x in images:
            refgptstr += ' '
            refgptstr += str(x)

        payload2 += " Data: " + gptstring
        payloadimg = f" Now, with the above data, I will provide you with some image links relating to {word}."
        payloadimg += f" Do filter through all the data and give me ANY relevant links. Here is the data: {refgptstr}."
        payload2 += " " + payloadimg
    else:
        # Taking elements 0-4 in results list 
        for x in results[1:6]:
            gptstring += ' '
            gptstring += str(x)
        # Taking elements 5-9 in results list
        for y in results[5:11]:
            gptstring2 += ' '
            gptstring2 += str(y)

        # print(gptstring)
        # print(gptstring2)
        payload2 += " Data: " + gptstring
        payload3 += " Here is some more data to add onto the the report. Remember to KEEP your previous response and ADD ON! Data: " + gptstring2
        

def chat(payload1, payload2, payload3):
   global messages
   messages.append({"role": "user", "content": payload1})
   response = client.chat.completions.create(
            messages=messages,
            model="Meta-Llama-3-70b-instruct",
        )
   gpt_response = response.choices[0].message.content
#    print(gpt_response)
   messages.append({"role": "assistant", "content": payload2})
   response = client.chat.completions.create(
            messages=messages,
            model="Meta-Llama-3-70b-instruct",
        )
   gpt_response = response.choices[0].message.content
#    print(gpt_response)
   messages.append({"role": "assistant", "content": payload3})
   response = client.chat.completions.create(
            messages=messages,
            model="Meta-Llama-3-70b-instruct",
        )
   gpt_response = response.choices[0].message.content
   print(gpt_response)


def email_address(email):
    url = "https://webapi.namescan.io/v1/freechecks/email/breaches"

    payload = {"email": email}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print()
        print("Email Breaches: ")
        print()
        data = response.json()
        breaches = data.get("breaches", [])
        filtered_breaches = []

        seen_titles = set()

        for breach in breaches:
            title = breach.get("title", "Unknown")
            if title not in seen_titles:
                seen_titles.add(title)
                filtered_breaches.append({
                    "Title": title,
                    "Date": breach.get("date", "Unknown"), 
                    "Description": breach.get("description", "No description available"),
                })

        for breach in filtered_breaches:
            print(f"Title: {breach['Title']}")
            print(f"Date: {breach['Date']}")
            print(f"Description: {breach['Description']}\n")
    else:
        print(
            f"Error: Unable to fetch data (Status Code: {response.status_code})"
        )

def instagram_api(insta):

	url = "https://instagram-scraper-api2.p.rapidapi.com/v1/info"

	querystring = {"username_or_id_or_url": insta}

	headers = {
		"x-rapidapi-key": "7cef9caf7emshbcd7d852995df3cp114277jsn623179640e47",
		"x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	print(response.json())

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    d = OSINT(root)
    if d.result:  # Check if the dialog returned a result
        word, add, img, email, insta= d.result
        start_time = time.time()

        payload_gen(word, add, img)
        print("Please wait a while...")
        print()
        chat(payload, payload2, payload3)
        email_address(email)
        # beta testing of instagram api
        # instagram_api(insta)
        end_time = time.time()
        time_taken = end_time - start_time
        print()
        print("Request completed in " + str(time_taken) + "s")
    else:   
        print("Please input the necessary information.")


main()

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt 4 api
