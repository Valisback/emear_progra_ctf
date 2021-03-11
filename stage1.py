from env import config
import requests
import json

base_url = config['MERAKI_BASE_URL']
endpoint_url = "/organizations"

header = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

global_url = f"{base_url}{endpoint_url}"

## Retrieving list of organizations and picking the one with the name we are looking for.
## Collecting its ID to use it for future requests

response = requests.get(url = global_url, headers = header)

orgName = "DevNet Sandbox"
orgId = 0
orgRetrieved = False

if response.status_code == 200:
    print("\nSuccessfully retrieved organizations!\n")
    resp = response.json()
    for org in resp:
        if(org["name"] == orgName):
            orgRetrieved = True
            orgId = org["id"]
            break
        orgRetrieved = False
else:
    print("Error {}".format(response.status_code))
    orgRetrieved = False

## Retrieving list of networks belonging to the organization ID specified above
## Collecting the ID of the network with the name we are looking for

netName = "DevNet Sandbox ALWAYS ON"
netId = 0
netRetrieved = False

if orgRetrieved:
    endpoint_url = f"/organizations/{orgId}/networks"
    global_url = f"{base_url}{endpoint_url}"
    response = requests.get(url = global_url, headers = header)
    if response.status_code == 200:
        print("\nSuccessfully retrieved networks of org with Id: {}\n".format(orgId))
        resp = response.json()
        for network in resp:
            if(network["name"] == netName):
                netRetrieved = True
                netId = network["id"]
                break
            netRetrieved = False
else:
    print("Problem retrieving organization")

## Retrieving list of all available devices in the network specified above
## Collecting their name, type, mac address, and serial

data = {}
data['devices'] = []

if netRetrieved:
    endpoint_url = f"/networks/{netId}/devices"
    global_url = f"{base_url}{endpoint_url}"
    response = requests.get(url = global_url, headers = header)
    if response.status_code == 200:
        print("\nSuccessfully retrieved devices of network with Id: {}\n".format(netId))
        resp = response.json()
        for device in resp:
            elem = {}
            if ("name" in device):
                elem["name"] = device["name"]
            if ("serial" in device):
                elem["serial"] = device["serial"]
            if ("mac" in device):
                elem["mac"] = device["mac"]
            if ("model" in device):
                elem["model"] = device["model"]  

            data['devices'].append(elem)

else:
    print("Problem retrieving network")

## Printing the result into a json file:

with open('devices.json', 'w') as outfile:
    json.dump(data, outfile)