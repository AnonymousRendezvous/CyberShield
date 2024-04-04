from duckduckgo_search import DDGS
from g4f.client import Client

word = input("Query: ")
new = '"' + word + '"'
# addnew = input("Query 2:")
# temp = word + ' ' + addnew + ' ' + "site:https://issuu.com"
results = DDGS().text(new, max_results=100)
# Where results is a dictionary

# if results == []:s
#     count = len(new.split())
    
# print(results)


payload =  "If I gave you some information on someone, could you write me a report on them?"
payload += " Here is the data with some helpful links. Do note that the person's name is" + word + ", perhaps you could also create a web of people relating to " + word

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



# Additional features to implement:
#     Include additional results on the person
#     Rerun the program to ensure reliability + get more info
#     Implement "cross searching" (when full name is not in proper order, results vary)
#     Fine tune GPT commands
#     Create "web of interactions" --> person's close friends/family
#     Implement other API's like Facebook, instagram, X... for more info trawling
#     Integrate images feature
#     Integrate maps feature with images feature to determine exact location
#     Integrate reverse image tracing(if possible)

# Special thanks to:
# https://github.com/xtekky/gpt4free, for providing free gpt api

