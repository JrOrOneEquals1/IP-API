# Flask, to receive original request
from flask import Flask, request
# Json, to parse str to dict
import json
# Requests, to send requests to the API and get data back
import requests
from gunicorn

# Open file with urls and API keys
info = open('info.txt', 'r').readlines()
# Assign lines in file to specific variables
whoisURL = info[0]
whoisKey = info[1]
vtURL = info[2]
vtKey = info[3]

# Init the app
app = Flask(__name__)

# Set endpoint to be railway URL (ip-api-production.up.railway.app)
# Function gets called when a POST request is received at above address
@app.route('/', methods=['POST', 'GET'])
def result():
    # Parse request data into python dict
    data = json.loads(request.data)
    # Get type of value passed in (ip/domain/hash) case insensitive
    contentType = data['type'].lower()
    # Get value passed in, case sensitive
    content = data['content']
    # If type is ip or domain
    if contentType in ['ip', 'domain']:
        # Send request to WhoIs API to get info about ip or domain
        info = requests.post(f'{whoisURL}?apiKey={whoisKey}&domainName={content}&outputFormat=JSON').text
    # If type is a file hash
    elif contentType == 'hash':
        # Send request to VirusTotal API to get info about the hash
        info = requests.get(f'{vtURL}{content}', headers={'x-apikey': f'{vtKey}'}).text
    else:
        # If type isn't ip/domain/hash
        return f"Invalid type passed in: '{contentType}'"
    # Return the retrieved info as dict
    return json.loads(info)

# Start the flask app (for dev env)
# app.run()