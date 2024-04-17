# pip install duckduckgo_search
from duckduckgo_search import DDGS
# pip install -U g4f
from g4f.client import Client
import threading

# Important to note that only one query to GPT is available per request --> might need to integrate threading

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


#payload for first search
payload =  "If I gave you some information on someone, could you write me a comprehensive report on them?"
payload += " Do note that the person's name is" + word + ", perhaps you could also create a web of people relating to " + word + ", and provide ANY and ALL links where the information can be found."
payload += "Do also see if you can extract basic information such as past and current education statuses, location and information from ANY accounts like their username or email."
payload += "Lastly, also note that " + add 
payload += " Here is the data with links (to be included): \n."

gptstring = ""
# refined gpt string
refgptstr = ""

#iterating through dictionary

if img == "y":
    for x in results:
        gptstring += ' '
        gptstring += str(x)
    
    for x in images:
        refgptstr += ' '
        refgptstr += str(x)
else:
    for x in results:
        gptstring += ' '
        gptstring += str(x)


payload += " Data: " + gptstring

#payload for images
payloadimg = "Now, with the above data, I will provide you with some image links relating to " + word
payloadimg += ". Do filter through all the data and give me ANY relevant links. Here is the data: " + refgptstr

finalpayload = ""

if img == "y":
  finalpayload += payload + " " + payloadimg
else:
  finalpayload += payload

storenum = 0
storemsg = ""

def chat(finalpayload):
    client = Client()
    response = client.chat.completions.create(
        model = "openchat_3.5",
        messages=[{"role": "user", "content": finalpayload}]
    )
    #accessing global values outside function
    global storenum
    global storemsg
    print(response.choices[0].message.content)
    if len(response.choices[0].message.content) > storenum:
        storenum = len(response.choices[0].message.content)
        storemsg = str(response.choices[0].message.content)
    
    
# Threading implementation (submit multiple responses to chat gpt)
for x in range(details):
    print("This will take a while, please wait...")
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

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt 3.5 api
