import requests
import time
import json
import configparser
from fake_useragent import UserAgent
from requests.exceptions import RequestException
import random

URL = "https://api.discord.gx.games/v1/direct-fulfillment"
UID = {"partnerUserId": "69f7b7c20983f391d4ea2726da99f7144828e4f6136308f11b254c2ded43c556"}
BASE_URL = "https://discord.com/billing/partner-promotions/1180231712274387115/"
SETTINGS = configparser.ConfigParser()
SETTINGS.read("settings.ini")
UA = UserAgent()

# Generate a random User-Agent string
random_user_agent = UA.random

headers = {
    "User-Agent": random_user_agent
}

def getToken() -> str:
    try:
        response = requests.post(URL, json=UID, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses

        data = json.loads(response.text)
        return data["token"]
    except RequestException as e:
        print(f"Error: {e}")
        return None

links = set()

try:
    for number in range(int(SETTINGS["DEFAULT"]["GenerationAmount"])):
        token = getToken()

        if token is not None:
            links.add(BASE_URL + token)
            print(f"Generated Token #{number + 1}. Press CTRL+C to stop and write links to links.txt.")
        
        time.sleep(int(SETTINGS["DEFAULT"]["Cooldown"]))
except KeyboardInterrupt:
    pass

with open("links.txt", "w") as file:
    file.write("\n".join(links)) # Tokens are written to the links.txt file upon closing the program.

print("\nLINKS WRITTEN TO links.txt")
