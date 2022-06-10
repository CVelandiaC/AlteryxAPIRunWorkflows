
from Alteryx_Execute_WF_Fun import *
import json 


with open('Alteryx_creds.json') as json_file:
    creds = json.load(json_file)

DataFLow_ID = "XXXXXX"
Req_body = '{"priority" : "3"}' # Change priority of flow execution.

# Alteryx API Call Body Example
"""{
    "questions": [
    {
      "name": "question1name",
      "value": "question1value"
    }],
    "priority" : "3"
}
"""

Response = execute_workflow(creds["Key"], creds["Secret"], creds["Gallery"], DataFLow_ID,  Req_body)

# Parse respnse and print it
Pretty_response = json.dumps(Response, sort_keys=True, indent=4, ensure_ascii=False)
print(Pretty_response)

# Save Response
with open('Alteryx_Response.json', 'w') as outfile:
    json.dump(Response, outfile, ensure_ascii=False)