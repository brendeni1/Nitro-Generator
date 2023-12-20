import requests
import time
import json
import configparser

URL = "https://api.discord.gx.games/v1/direct-fulfillment"
UID = {"partnerUserId": "69f7b7c20983f391d4ea2726da99f7144828e4f6136308f11b254c2ded43c556"}
BASE_URL = "https://discord.com/billing/partner-promotions/1180231712274387115/"
SETTINGS = configparser.ConfigParser()
SETTINGS.read("settings.ini")

def getToken() -> str:
    response = requests.post(URL, json=UID)

    data = json.loads(response.text)

    return data["token"]

links = set()

try:
    for number in range(int(SETTINGS["DEFAULT"]["GenerationAmount"])):
        token = getToken()

        links.add(BASE_URL + token)

        print(f"Generated Token #{number + 1}. Press CTRL+C to stop and write links to links.txt.")
        
        time.sleep(int(SETTINGS["DEFAULT"]["Cooldown"]))
except KeyboardInterrupt:
    pass

with open("links.txt", "w") as file:
    file.write("\n".join(links)) # Tokens are written to the links.txt file upon closing the program.

    print("\nLINKS WRITTEN")