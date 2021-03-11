from env import config
import requests


base_url = config['MERAKI_BASE_URL']
endpoint_url = "/organizations"

header = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

global_url = f"{base_url}{endpoint_url}"

response = requests.get(url = global_url, headers = header)

if response.status_code == 200:
    print("Successful! \n===== List of organizations: =====\n\n")
    resp = response.json()
    for org in resp:
        print("ID: {} \nName: {} \n=============\n".format(org["id"], org["name"]))
else:
    print("Error {}".format(response.status_code))
