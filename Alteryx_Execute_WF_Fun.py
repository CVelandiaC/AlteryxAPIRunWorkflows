
import random
import urllib
import urllib.parse
from hashlib import sha1
import hmac
import requests
import base64
import time
import json


def alteryx_oauth_auth(apikey, apisecret, url, method, vals):

    # Generate time and nonce fields
    oauth_nonce = str(random.randint(0,51543575)+654987) # Generate nonce random parameter
    oauth_timestamp = str(int(time.time())) # Generate timestamp 

    # Generate Auth String using HMAC-SHA1 method

    values = str('oauth_consumer_key=' + apikey +'&oauth_nonce=' + oauth_nonce + '&oauth_signature_method=HMAC-SHA1&oauth_timestamp=' + oauth_timestamp + '&oauth_version=1.0')
    
    # percent encoding
    percent_values = urllib.parse.quote(values, safe='')
    percent_url = urllib.parse.quote(url, safe='')

    # create signature_base_string and encode as bytes
    Signature_Base_String = method + '&' + percent_url + '&' + percent_values

    # encode the signature and secret as bytes
    raw =  bytes(Signature_Base_String, 'utf-8')
    key = bytes(apisecret+'&', 'utf-8')

    # hmac-sha1 encryption to generate oauth signature
    hashed = hmac.new(key, raw, sha1)
    raw = base64.urlsafe_b64encode(hashed.digest())
    oauth_signature = raw.decode()

    oauth_signature = oauth_signature.replace('-','+')
    oauth_signature = oauth_signature.replace('_', '/')

    oauth_signature = urllib.parse.quote(oauth_signature, safe='')

    oauth_signature = 'oauth_signature=' + oauth_signature

    # generate the signed url and return it
    #url = url + '?' + vals + values + '&' + oauth_signature
    if vals == "":
        url = url + '?' + vals + values + '&' + oauth_signature
    else: 
        url = url + values + '&' + oauth_signature

    print(url)
    return url


def execute_workflow_return_result(apikey, apisecret, baseurl, workflowid, payload):

    # create the url required as per this call, this includes the workflow id passed by the user
    url = baseurl + 'api/v1/workflows/' + workflowid + '/jobs/'
    method = 'POST'

    # use the ayx_auth function created above to create a signed url
    url = alteryx_oauth_auth(apikey, apisecret, url, method, "")

    # make the initial api call to trigger the job to run
    headers = {'Content-type': 'application/json'}

    apicall = requests.post(url, data=payload, headers=headers)

    # Only proceed if the respose from the api was 200 (i.e. things are fine!)

    if apicall.status_code == 200:

        # retrieve the jobid from the response
        jsonresponse = apicall.json()
        jobid = jsonresponse['id']

        with open('Alteryx_Run_WF_Response.json', 'w') as outfile:
            json.dump(jsonresponse, outfile, ensure_ascii=False)

        _, apiresponse = get_job_status(baseurl, jobid, apikey, apisecret)        

        # loop to keep fetching the job status until it is set to complete
        while apiresponse['status'] != 'Completed':

            # hold the call for 5 seconds so that we aren't constantly querying
            time.sleep(5)

            apicall, apiresponse = get_job_status(baseurl, jobid, apikey, apisecret)

            # check if the status code is 200 if not break the loop
            if apicall.status_code != 200:
                break

            # once the call has returned the status 'completed' go and fetch the full apiresponse

        else:

            _, apiresponse = get_job_status(baseurl, jobid, apikey, apisecret)
            
            return apiresponse
    else:
        # In case of error launching the workflow display the response
        apiresponse = apicall.json()

        return apiresponse

def get_job_status(baseurl, jobid, apikey, apisecret):
    # create the url required to check the status of the generated job
    url = baseurl + 'api/v1/jobs/' + jobid + '/'
    method = 'GET'

    # use the ayx_auth function created above to create a signed url
    signedurl = alteryx_oauth_auth(apikey, apisecret, url, method, "")

    # make the request to fetch the job status
    apicall = requests.get(signedurl)
    apiresponse = apicall.json()

    return [apicall, apiresponse]

def get_workflow_jobs(baseurl, workflowid, apikey, apisecret, sortfield, direction, offset, limit):
     # create the url required as per this call, this includes the workflow id passed by the user
    Extra_vals = 'sortField=' + sortfield + '&direction=' + direction + '&offset=' + offset + '&limit=' + limit + '&' 
    #url = baseurl + 'api/v1/workflows/' + workflowid + '/jobs/?' + Extra_vals
    url = baseurl + 'api/v1/workflows/' + workflowid + '/jobs/'
    method = 'GET'

    # use the ayx_auth function created above to create a signed url
    url = alteryx_oauth_auth(apikey, apisecret, url, method, "")

    # make the initial api call to trigger the job to run
    headers = {'Content-type': 'application/json'}

    apicall = requests.post(url, headers=headers)
    apiresponse = apicall.json()

    return [apicall, apiresponse]