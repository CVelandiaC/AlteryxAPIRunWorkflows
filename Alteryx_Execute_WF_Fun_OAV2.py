import requests
import json

##############################################
############### GET AUTH TOKEN ###############
##############################################

with open('Alteryx_Creds.json') as json_file:
    creds = json.load(json_file)


# Auth variables
apiKey = creds["Key"]
apiSecret = creds["Secret"]
authUrl = 'https://alteryx.adl-analytics.net/webapi/oauth2/token'

# Request auth token
response = requests.post(
    authUrl,
    data = {
        'grant_type':'client_credentials',
        'client_id' : apiKey,
        'client_secret' : apiSecret
    }
)

print(response.text)

# Parse the access token
response = json.loads(response.text)
print(response)
token = response['access_token']
print(token)
##############################################
###### MAKE A REQUEST TO THE SERVER API ######
##############################################

requestUrl = 'https://alteryx.adl-analytics.net/webapi/v3/collections'
headers = {'Authorization' : 'Bearer ' + token}

collections = requests.request('GET',
                              requestUrl,
                              headers=headers)

collections = json.loads(collections.text)
print(collections)