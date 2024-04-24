# pip install duckduckgo_search
from duckduckgo_search import DDGS
# pip install -U g4f
from g4f.client import Client
import threading
import sys
import os

# Suppress stderr output by redirecting it to os.devnull
sys.stderr = open(os.devnull, 'w')

word = input("Query: ")
add = input("Any other information: ")
img = input("Do you want to trawl for images? (beta testing) y/n: ")
details = int(input("How detailed do you want your report to be? (1-10): "))

new = '"' + word + '"'

if img == "y":
    results = DDGS().text(new, max_results=25)
    images = DDGS().images(new, region="sg-en", max_results=25)
else:
    results = DDGS().text(new, max_results=50)


#Global variables

finalpayload = ""
storenum = 0
storemsg = ""

#function for generating final payload
def payload_gen(word, add):
    global finalpayload
    payload = f"If I gave you some information on someone, could you write me a comprehensive report on them?"
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





#function for generating response
def chat(finalpayload):
    client = Client()
    response = client.chat.completions.create(
        model = "airoboros-70b",
        messages=[{"role": "user", "content": finalpayload}]
    )
    #accessing global values outside function
    global storenum
    global storemsg
    if len(response.choices[0].message.content) > storenum:
        storenum = len(response.choices[0].message.content)
        storemsg = str(response.choices[0].message.content)


payload_gen(word, add)

# Threading implementation (submit multiple responses to chat gpt)
for x in range(details):
    print("This will take a while, please wait...")
    # to fix coro async runtime error in future
    t1 = threading.Thread(target=chat, args=(finalpayload,))
    t2 = threading.Thread(target=chat, args=(finalpayload,))
    t3 = threading.Thread(target=chat, args=(finalpayload,))
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

print("")
print(storemsg)
