# Alteryx_API_Execute_Flows
Functions to execute alteryx work flows programatically using API V1/V2 which uses OAUTH 1 for authentication. The process is teh following:

Both v1 and v2 endpoints use the same OAuth1.0a method to sign every single request, and therefore don't reuse a token or signature when sending multiple requests. This OAuth1.0a method relies on "signing" a request by generating a string which contains most of the details about the request, including the base URL, serialized parameters, a random nonce, timestamp, and API Access Secret. The resulting string is hashed with HMAC-SHA1, and that "signature" is sent along as an additional parameter with the actual request, minus the API Access Secret. When the Server successfully rebuilds the signature from the provided values plus the local API Access Secret, then Server knows the client had the correct secret and that the request had not been tampered with.  

API Response Codes:
200	Success	
401	The provided API Key (oauth_consumer_key) is invalid.	
401	The provided signature (oauth_signature) is invalid.

For Security Alteryx API Credentials are read from the Alteryx_creds.json file with keys:
Gallery
Key 
Secret

Based on Ben Moss Code and [article](https://www.theinformationlab.co.uk/2021/02/15/trigger-an-alteryx-workflow-app-to-run-upon-loading-data-to-s3/)
