# pip install duckduckgo_search
from duckduckgo_search import DDGS
# pip install -U g4f
from g4f.client import Client

# Important to note that only one query to GPT is available per request --> might need to integrate threading

word = input("Query: ")
add = input("Any other information: ")
img = input("Do you want to trawl for images? (beta testing) y/n: ")
new = '"' + word + '"'

if img == "y":
    results = DDGS().text(new, max_results=50)
    images = DGGS().images(word, region="sg-en", max_results=50)
else:
    results = DDGS().text(new, max_results=100)


#payload for first search
payload =  "If I gave you some information on someone, could you write me a comprehensive report on them?"
payload += " Do note that the person's name is" + word + ", perhaps you could also create a web of people relating to " + word + ", and provide the links where the information can be found."
payload += "Do also see if you can extract basic information such as past and current education statuses, location and information from certain accounts like their username or email."
payload += "Lastly, also note that " + add 
payload += " Here is the data with links: \n."

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

client = Client()
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[{"role": "user", "content": finalpayload}]
)
print("")
print(response.choices[0].message.content)

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt 3.5 api
