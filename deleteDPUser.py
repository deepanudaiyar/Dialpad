import requests
import json
import sys

#Searches by user email & pass the username and key as system arguments to the script
userEmail = sys.argv[1]
key = sys.argv[2]

print(f"Searching Dialpad for {userEmail}. Please wait...")
print('')

url = "https://dialpad.com/api/v2/users"

querystring = {"email":str(userEmail),"state":"active","limit":"10","apikey":f"{key}"}

headers = {'accept': 'application/json'}

response = requests.request("GET", url, headers=headers, params=querystring)

userData = json.loads(response.text)

userID = userData['items'][0]['id']

print("User found!!")
print('')

#Delete a user by id

url = f"https://dialpad.com/api/v2/users/{userID}"

querystring = {"apikey":f"{key}"}

headers = {'accept': 'application/json'}

response = requests.request("DELETE", url, headers=headers, params=querystring)

responseData = json.loads(response.text)

print(responseData)
print('')
print(f"{userEmail} has been deleted from Dialpad")
