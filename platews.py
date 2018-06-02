import requests
import json

def checkForPlateExistence(plate):
    url = 'http://localhost:8080/plates/checkforexistence'
    data = {'plate': plate }
    response = requests.post(url, data=data)

    obj = json.loads(response.text)
    print(obj['success'])
        

    return response
