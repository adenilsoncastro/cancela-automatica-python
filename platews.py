import requests
import json
import base64

def checkForPlateExistence(plate):

    with open(r"C:\Users\oluis\Desktop\TCC\cancela-automatica-python\gol51_threshold.png", "rb") as image_file:
        img = base64.b64encode(image_file.read())

    url = 'http://localhost:8080/plates/checkforexistence'
    data = {'plate': plate, 'img': img }
    response = requests.post(url, data=data)

    obj = json.loads(response.text)
    print(obj['success'])
        

    return response

checkForPlateExistence('ayh-2598')