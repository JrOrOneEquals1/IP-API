# Flask, to receive the request
from flask import Flask, request
# Json, to parse str to obj
import json
# Requests, to send requests to the API and get data
import requests

# Init the app
app = Flask(__name__)

# Set endpoint to be railway URL (ip-api-production.up.railway.app)
# Function gets called when a POST request is received at above address
@app.route('/', methods=['POST'])
def result():
    # Parse request data into python dict
    data = json.loads(request.data)
    # Get type of value passed in (ip/domain/hash) case insensitive
    contentType = data['type'].lower()
    # Get value
    content = data['content']
    # If type is ip or domain
    if contentType in ['ip', 'domain']:
        # Send request to WhoIs API to get info about ip or domain
        info = requests.post(f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_sKqg6zX9HGSFXMrIXU4l8DwVTnE2C&domainName={content}&outputFormat=JSON').text
        # Return the retrieved info as dict
        return json.loads(info)
    # If type is hash
    if contentType == 'hash':
        # Send request to VirusTotal API to get info about the hash
        info = requests.get(f'https://www.virustotal.com/api/v3/files/{content}', headers={'x-apikey': 'a9442725b4f377c0d308c043adf6ced518728174368f0d32b16a53fba621af4b'}).text
        # Return the retrieved info as dict
        return json.loads(info)

# Start the flask app
app.run()