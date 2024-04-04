from duckduckgo_search import DDGS
from g4f.client import Client

word = input("Query: ")
add = input("Any other information: ")
new = '"' + word + '"'
results = DDGS().text(new, max_results=200)

    
print(results)


payload =  "If I gave you some information on someone, could you write me a comprehensive report on them?"
payload += " Do note that the person's name is" + word + ", perhaps you could also create a web of people relating to " + word + ", and provide the links where the information can be found."
payload += "Do also see if you can extract basic information such as past and current education statuses, location and information from certain accounts like their username or email."
payload += "Lastly, also note that " + add 
payload += " Here is the data with links: \n."

gptstring = ""

for x in results:
    gptstring += ' '
    gptstring += str(x)

payload += " Data: " + gptstring

client = Client()
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[{"role": "user", "content": payload}]
)
print("")
print(response.choices[0].message.content)

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt api
