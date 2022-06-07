from Alteryx_Execute_WF_Fun import *
import json 

# Código tomado de https://www.theinformationlab.co.uk/2021/02/15/trigger-an-alteryx-workflow-app-to-run-upon-loading-data-to-s3/

with open('Alteryx_creds.json') as json_file:
    creds = json.load(json_file)

DataFLow_ID = "618d71a16bfa0f31885bf80d"
Req_body = '{"priority" : "3"}'

#Ejemplo llamado de apps de alteryx
"""{
    "questions": [
    {
      "name": "question1name",
      "value": "question1value"
    }],
    "priority" : "3"
}
"""

Response = execute_workflow(creds["Key"], creds["Secret"], creds["ADL_Gallery"], DataFLow_ID,  Req_body)
Pretty_response = json.dumps(Response, sort_keys=True, indent=4, ensure_ascii=False)
print(Pretty_response)

# Save Response
with open('Alteryx_Response.json', 'w') as outfile:
    json.dump(Response, outfile, ensure_ascii=False)