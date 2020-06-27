import requests
import pandas as pd
import getpass
import json
import sys
accountName = getpass.getuser()

#importing API key as system arguments
key = sys.argv[1]

print('Gathering user details, please wait...')
print('')

#reads csv file to get email address and user details
df = pd.read_csv(f'/Users/{accountName}/Documents/GAMfiles/newUser.csv')

#retrieves few key details and saves into a variable.
userEmail = df.loc[0]['email']
first = df.loc[0]['first']
last = df.loc[0]['last']

#Creating a user in Dialpad 
print(f'Creating a Dialpad account for {userEmail}. Please wait...')

url = "https://dialpad.com/api/v2/users"

querystring = {"apikey":f"{key}"}

payload = '{\"license\":\"talk\",\"email\":\"'+str(userEmail)+'\",\"first_name\":\"'+str(first)+'\",\"last_name\":\"'+str(last)+'\",\"office_id\":\"000111\"}'
headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

newUserData = json.loads(response.text)

userID = newUserData['id']

print('')
print(f'{userEmail} account created')
print('')

# Sorting thru list of available numbers and selects a number with preferred area code
url = "https://dialpad.com/api/v2/numbers"

areaCode = input(f'What is the preferred area code for {first} {last}? :')

print('')
print(f'Getting available numbers for your area code {areaCode}. Please wait...')
print('')

querystring = {"limit":"500","status":"available","apikey":f"{key}"}

headers = {'accept': 'application/json'}

response = requests.request("GET", url, headers=headers, params=querystring)

availableNumbers = json.loads(response.text)

def find_number(availableNumbers):
    for item in availableNumbers['items']:
        if item['area_code'] == areaCode:
            num = item['number']
            return num
    
    return None

    
num = find_number(availableNumbers)
while not num and availableNumbers.get('cursor'):
    querystring['cursor'] = availableNumbers.get('cursor')
    response = requests.request("GET", url, headers=headers, params=querystring)
    availableNumbers = json.loads(response.text)
    num = find_number(availableNumbers)
    


# Assigning retrieved number to user 

url = f"https://dialpad.com/api/v2/users/{userID}/assign_number"

querystring = {"apikey":f"{key}"}

payload = '{\"number\":\"'+str(num)+'\"}'
headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

# Formatting phone number to a standard format for use in signature
fNum = str(num)

fNum = fNum[2:]

def phone_format(n):                                                                                                                                  
    return format(int(n[:-1]), ",").replace(",", ".") + n[-1]

fNum = phone_format(fNum)

print(f'{userEmail} has been provisioned in Dialpad with {fNum}')

