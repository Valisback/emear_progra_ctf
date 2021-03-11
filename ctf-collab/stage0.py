import requests

from env import config

s = requests.Session()

s.headers.update({
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
})


# Verify api access
WEBEX_BASE_URL = config['WEBEX_BASE_URL']

url = f"{WEBEX_BASE_URL}/v1/rooms"

room_id = 0

try:
    resp = s.get(url)
    if resp.status_code == 200:
        for room in resp.json()["items"]:
            if(room["title"] == "CSAP Programmability CTF - Team 2"):
                #print(room)
                room_id = room["id"]


except Exception as e:
    print(e)

if room_id != 0:
    print("Room ID: ", room_id)
else:
    print("Error retrieving room ID")