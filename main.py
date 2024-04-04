from duckduckgo_search import DDGS
from g4f.client import Client

word = input("Query: ")
new = '"' + word + '"'
results = DDGS().text(new, max_results=100)


payload =  "If I gave you some information on someone, could you write me a report on them?"
payload += " Here is the data with some helpful links. Do note that the person's name is" + word + ", perhaps you could also create a web of people relating to " + word + ", and provide the links where the information can be found"

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

#MIT licence

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt api

