import requests

from env import config


headers = {
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
}


# Verify api access
WEBEX_BASE_URL = config['WEBEX_BASE_URL']

url = f"{WEBEX_BASE_URL}/v1/rooms"

myRoom = {
    "title": "CTF-collab Team Valentin"
}

add_emails = ["mneiding@cisco.com", "frewagne@cisco.com"]

try:
    resp = requests.post(url = url, headers = headers, data=myRoom)
    if resp.status_code == 200:
        room_id = resp.json()["id"]
        print("Room Created! ", room_id)
        try:
            url = f"{WEBEX_BASE_URL}/v1/memberships"
            for addr in add_emails:
                body = {
                    "roomId": room_id,
                    "personEmail": addr
                }
                resp = requests.post(url = url, headers = headers, data=body)
                if resp.status_code == 200:
                    print("Member added: ", resp.json()["personEmail"])
            try:
                url = f"{WEBEX_BASE_URL}/v1/messages"
                markdown = "** Welcome Everyone ** Here is the room created for the ctf-collab lab! Warmest welcome to: "   
                for addr in add_emails:
                    markdown = markdown + addr + " "

                body = {
                    "roomId": room_id,
                    "markdown": markdown
                }
                resp = requests.post(url = url, headers = headers, data=body)
                if resp.status_code == 200:
                    print("Message posted: ", resp.json()["markdown"])
            except Exception as e:
                print(e)  
        except Exception as e:
            print(e)
    else:
        print(resp.status_code, resp.json())

except Exception as e:
    print(e)
