import requests
import json
import base64

def checkForPlateExistence(plate):

    with open(r"C:\Users\oluis\Desktop\TCC\cancela-automatica-python\car12_threshold.png", "rb") as image_file:
        img = base64.b64encode(image_file.read())

    url = 'http://ec2-54-218-220-67.us-west-2.compute.amazonaws.com:8080/plates/checkforexistence' 
    # url = 'http://localhost:8080/plates/checkforexistence'
    data = {'plate': plate, 'img': img , 'barrierId': 1}
    response = requests.post(url, data=data)

    obj = json.loads(response.text)
    print(obj['success'])
        

    return response

checkForPlateExistence('ABC-1234')