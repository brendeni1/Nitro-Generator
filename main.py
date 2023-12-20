import requests
import time
import json
import configparser
from fake_useragent import UserAgent
from requests.exceptions import RequestException
import random
import traceback

URL = "https://api.discord.gx.games/v1/direct-fulfillment"
UID = {"partnerUserId": "69f7b7c20983f391d4ea2726da99f7144828e4f6136308f11b254c2ded43c556"}
BASE_URL = "https://discord.com/billing/partner-promotions/1180231712274387115/"
SETTINGS = configparser.ConfigParser()
ua = UserAgent()
SETTINGS.read("settings.ini")

# Generate a random User-Agent string
random_user_agent = ua.random

headers = {
    "User-Agent": random_user_agent
}

error_count = 0  # Initialize error count
cooldown_start_time = None  # Initialize cooldown start time

def getToken() -> str:
    global cooldown_start_time  # Declare cooldown_start_time as a global variable
    global error_count  # Declare error_count as a global variable

    try:
        response = requests.post(URL, json=UID, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses

        data = json.loads(response.text)
        return data["token"]
    except RequestException as e:
        error_count += 1

        # Check if error count exceeds 2 within 10 seconds
        if error_count >= 2:
            current_time = time.time()
            if cooldown_start_time is None:
                cooldown_start_time = current_time
            elif current_time - cooldown_start_time <= 10:
                # Display a cooldown animation in the terminal
                while current_time - cooldown_start_time <= 10:
                    remaining_time = 10 - (current_time - cooldown_start_time)
                    print(f"Cooldown: {remaining_time:.1f} seconds remaining", end="\r")
                    time.sleep(1)
                    current_time = time.time()
                print("Cooldown: Done.                         ")  # Clear the cooldown message
                error_count = 0
                cooldown_start_time = None
        return None

links = []

try:
    # Read the last generated number from a file
    try:
        with open("last_generated_number.txt", "r") as num_file:
            last_generated_number = int(num_file.read())
    except FileNotFoundError:
        last_generated_number = 0

    for number in range(last_generated_number, int(SETTINGS["DEFAULT"]["GenerationAmount"])):
        token = getToken()

        if token is not None:
            link = BASE_URL + token
            links.append(f"{number + 1}. Link: {link}")
            print(f"Generated Token #{number + 1}. Press CTRL+C to stop.")
        
        time.sleep(int(SETTINGS["DEFAULT"]["Cooldown"]))
except KeyboardInterrupt:
    pass
except Exception as e:
    # If an unhandled exception occurs, print the exception traceback
    traceback.print_exc()  # Print the exception traceback
    
    # Write the generated links to a "crash recovery" file
    with open("crash_recovery.txt", "w") as recovery_file:
        recovery_file.write("\n".join(links))  # Write generated links to the crash recovery file

# Write the last generated number to a file
with open("last_generated_number.txt", "w") as num_file:
    num_file.write(str(number))

with open("links.txt", "a") as file:
    file.write("\n".join(links)) # Tokens are written to the links.txt file upon closing the program.

print("\nLINKS WRITTEN TO links.txt")
