import json
import os
import sys
import time
import tkinter as tk
from tkinter import simpledialog

import g4f
import httpx
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from g4f.client import Client

# Suppress stderr output by redirecting it to os.devnull
sys.stderr = open(os.devnull, "w")


class OSINT(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Query:").grid(row=0)
        tk.Label(master, text="Enter a keyword associated with the person:").grid(row=1)
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
payloads = []

messages = []
http = []

# g4f client provider
client = Client(provider=g4f.Provider.MetaAI)


def extract_text_from_website(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        # Use httpx with cookies enabled and follow redirects (cookie interference with g4f library)
        with httpx.Client(headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()

            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script, style, and other non-content elements
            for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
                element.decompose()

            # Extract text from remaining elements
            text = soup.get_text(separator=" ", strip=True)

            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            cleaned_text = "\n".join(chunk for chunk in chunks if chunk)

            # Limit the text to 500 characters
            limited_text = cleaned_text[:500]

            return limited_text

    except httpx.HTTPStatusError as e:
        return f"HTTP Error: {e}"
    except httpx.RequestError as e:
        return f"Request Error: {e}"


def payload_gen(word, add, img):
    global payload, payload2, payload3, http
    new = '"' + word + '"'
    nadd = word + " " + add

    if img == "y":
        # Beta testing for images
        results = DDGS().text(new, max_results=3)
        images = DDGS().images(new, region="sg-en", max_results=2)
    else:
        results = DDGS().text(new, max_results=9)
        addresults = DDGS().text(nadd, max_results=3)

    payload = f"Write me a comprehensive report on a person that is as detailed as possible?"
    payload += f" Do note that the person's name is, {word}. Perhaps you could also create a web of people relating to them and provide ANY and ALL links where the information can be found."
    payload += "Do also see if you can extract basic information such as past and current education statuses, location and information from ANY accounts like their username or email."
    payload += f" Here is the data with links, do remember to INCLUDE AND NUMBER THE LINKS at the bottom: \n"
    gptstring = ""
    gptstring2 = ""
    gptstring3 = ""
    refgptstr = ""

    if img == "y":
        for x in results:
            gptstring += " "
            gptstring += str(x)

        for x in images:
            refgptstr += " "
            refgptstr += str(x)

        payload2 += " Data: " + gptstring
        payloadimg = f" Now, with the above data, I will provide you with some image links relating to {word}."
        payloadimg += f" Do filter through all the data and give me ALL relevant links. Here is the data: {refgptstr}."
        payload2 += " " + payloadimg
    else:
        # Check for duplicates in both lists
        for item in addresults[:]:
            if item in results:
                addresults.remove(item)
        # Taking elements 0-4 in results list
        for x in results[1:6]:
            gptstring += " " + str(x)
            if "href" in x:
                http.append(x["href"])

        # Taking elements 5-9 in results list
        for y in results[5:10]:
            gptstring2 += " " + str(y)
            if "href" in y:
                http.append(y["href"])
        # Taking elements in additional results
        for z in addresults:
            gptstring3 += " " + str(z)
            if "href" in z:
                http.append(z["href"])
        print("Results found: " + str(len(http)))

        http = [url for url in http if not url.lower().endswith(".pdf")]

        # Debugging DDGS
        if word.lower() == "debug" or add.lower() == "debug" or img.lower() == "debug":
            print(gptstring)
            print(gptstring2)
            print(gptstring3)
            for x in range(len(http)):
                print(http[x])

        payload2 += (
            " Do remember to include ALL links and make verbose inferences to the best of your ability! Here is some starting data for you. Data: "
            + gptstring
        )
        payload3 += (
            " Here is a final data check on the report. Clean up your report and remember to KEEP ALL content from your previous response(s) and ADD ON to everything especially the links at the bottom (numbered), being as VERBOSE as possible! Data: "
            + gptstring2
            + gptstring3
        )
        payloads.append(payload)
        payloads.append(payload2)
        for x in range(len(http)):
            key_content = extract_text_from_website(http[x])
            links = (
                "Now for each of the links you have identified, I will give you the content for each of them. Remember to ADD ON to your previous response, being as verbose as possible. Link: "
                + http[x]
                + " "
                + key_content
                + ". "
            )
            links += "KEEP ALL content from your PREVIOUS response(s), build upon them and analyse IN DETAIL the data provided with AS MUCH inferred information and proper organisation possible."
            payloads.append(links)
        payloads.append(payload3)


def chat(payloads):
    global messages
    messages = []  # Initialize the message history

    for i, payload in enumerate(payloads):
        # Add user message
        messages.append({"role": "user", "content": payload})

        # Get AI response
        response = client.chat.completions.create(
            messages=messages,
            model="Meta-Llama-3-70b-instruct",
        )
        gpt_response = response.choices[0].message.content
        # print(gpt_response)

        # Print last AI response
        if i == len(payloads) - 1:
            print(f"Response {i + 1}: ")
            print(gpt_response)


def email_address(email):
    url = "https://webapi.namescan.io/v1/freechecks/email/breaches"

    payload = {"email": email}
    headers = {"Content-Type": "application/json"}
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
                filtered_breaches.append(
                    {
                        "Title": title,
                        "Date": breach.get("date", "Unknown"),
                        "Description": breach.get("description", "No description available"),
                    }
                )

        for breach in filtered_breaches:
            print(f"Title: {breach['Title']}")
            print(f"Date: {breach['Date']}")
            print(f"Description: {breach['Description']}\n")
    else:
        print(f"Error: Unable to fetch data (Status Code: {response.status_code})")


def instagram_api(insta):
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/info"
    querystring = {"username_or_id_or_url": insta}
    headers = {
        "x-rapidapi-key": "7cef9caf7emshbcd7d852995df3cp114277jsn623179640e47",
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json().get("data", {})

    # Basic Profile Information
    username = data.get("username", "N/A")
    full_name = data.get("full_name", "N/A")
    is_private = data.get("is_private", False)
    is_verified = data.get("is_verified", False)
    follower_count = data.get("follower_count", "N/A")
    following_count = data.get("following_count", "N/A")
    media_count = data.get("media_count", "N/A")
    profile_pic_url = data.get("profile_pic_url", "")
    bio = data.get("biography", "")
    external_url = data.get("external_url", "")

    # Print Profile Summary
    print(f"Instagram Profile Summary\n{'-'*30}")
    print(f"Username: {username}")
    print(f"Full Name: {full_name}")
    print(f"Is Private: {'Yes' if is_private else 'No'}")
    print(f"Is Verified: {'Yes' if is_verified else 'No'}")
    print(f"Follower Count: {follower_count}")
    print(f"Following Count: {following_count}")
    print(f"Media Count: {media_count}")
    print(f"Profile Picture URL: {profile_pic_url}\n")

    # Print Biography and External Link
    print(f"Biography:\n{bio if bio else '(No Bio)'}")
    print(f"External URL: {external_url if external_url else '(No External URL)'}\n")

    # Additional Information
    print("Additional Information\n" + "-" * 30)
    guides_available = data.get("has_guides", False)
    fundraisers = data.get("active_standalone_fundraisers", {}).get("total_count", 0)
    downloads_enabled = data.get("third_party_downloads_enabled", 0)

    print(f"Guides Available: {'Yes' if guides_available else 'No'}")
    print(f"Standalone Fundraisers: {fundraisers}")
    print(f"Third Party Downloads Enabled: {'Yes' if downloads_enabled else 'No'}\n")

    # Location Data
    location_data = data.get("location_data", {})
    if location_data:
        city_name = location_data.get("city_name", "N/A")
        zip_code = location_data.get("zip", "N/A")
        latitude = location_data.get("latitude", "N/A")
        longitude = location_data.get("longitude", "N/A")
        print(f"Location Data:\n City: {city_name}\n Zip Code: {zip_code}\n Latitude: {latitude}\n Longitude: {longitude}\n")
    else:
        print("Location Data: Not Provided")


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    d = OSINT(root)
    if d.result:  # Check if the dialog returned a result
        word, add, img, email, insta = d.result
        start_time = time.time()
        payload_gen(word, add, img)
        print("Please wait a while...")
        print()
        chat(payloads)
        email_address(email)
        # Save instagram API uses
        if insta == "":
            print("Instagram username not filled in!")
        else:
            instagram_api(insta)
        end_time = time.time()
        time_taken = end_time - start_time
        print()
        print("Request completed in " + str(time_taken) + "s")
    else:
        print("Please input the necessary information.")


main()

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt 4 api
