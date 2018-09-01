import numpy as np
import cv2 as cv 
from PIL import Image
from camera import Camera
import pytesseract as ocr
from imageProcessing import ImageProcessing
from frame import Frame
from verificaPlaca import VerificaPlaca as vp
import platews as ws
import datetime
import time
import os
import sys
import RPi.GPIO as gpio
from RPLCD.gpio import CharLCD
import uuid

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.OUT)
gpio.setup(20, gpio.OUT)
gpio.setup(16, gpio.OUT)

lcd = CharLCD(pin_rs=18, pin_e=23, pins_data=[26,19,13,6], numbering_mode=gpio.BCM, cols=16, rows=2)

cap = cv.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 720)
count = 0

def image_name():
    return str(uuid.uuid4()).split('-')[0]

def open_gate(name,plate):
    cap.release()
    gpio.output(21, gpio.HIGH)
    time.sleep(.250)
    gpio.output(21, gpio.LOW)
    lcd.clear()
    lcd.cursor_pos=(0,0)
    lcd.write_string("Placa:")
    lcd.write_string(plate)
    lcd.cursor_pos=(1,0)
    lcd.write_string(name)
    time.sleep(5)
    cap.open(0)
    cap.set(3, 1080)
    cap.set(4, 720)

def log(text):
    with open("log.txt","a+") as file:
        file.write(text + "\n")
        file.close()

imgProcessing = ImageProcessing()
verificaPlaca = vp()

while(True): 
    ret, frame = cap.read()
    if ret == True:
        log("New frame captured at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    
        img = Frame(np.array(Image.fromarray(gray)), str(image_name()), None, None)
        log("Start processing frame " + str(img.name) + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("Start processing frame " + str(img.name) + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        img.image = imgProcessing.Billateral(img.image)
        img.image = imgProcessing.Canny(img.image)
        img.image = imgProcessing.GaussianBlur(img.image)
        imgProcessing.FindPossiblePlates(img)
        img.CropAllPlatesBorders()
        #img.validateAmountOfWhiteAndBlackPixels()        
        log("New frame " + str(img.name) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("New frame " + str(img.name) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))        
        if len(img.arrayOfPlates) > 0:
            log(str(len(img.arrayOfPlates)) + " possible plates found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
            print(str(len(img.arrayOfPlates)) + " possible plates found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
            for plate in enumerate(img.arrayOfPlates):
                _,plate[1].image = imgProcessing.ThresholdPlusOtsu(plate[1].image, 105)
                cv.imwrite("../processed/" + str(image_name()) + ".png", plate[1].image)
                result = ocr.image_to_string(Image.fromarray(plate[1].image), config="--psm 8")
                log("OCR finished processing for frame " + str(img.name) + ". Result: " + result + " - Time: " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))            
                print("OCR result: " + result)                
                placa = verificaPlaca.verificar(result)
                log("VP result: " + str(placa))
                print("VP result: " + str(placa))
                if not placa == -1:          
                    #api = ws.checkForPlateExistence(placa)
                    #if api == True:
                    #   open_gate(str(img.name),placa)
                    #   break
                    open_gate(str(img.name),placa)
                else:
                    gpio.output(16, gpio.HIGH)
                    time.sleep(.250)
                    gpio.output(16, gpio.LOW)
                    print("Plate not recognized")
                    log("Plate not recongnized")
        else:
            print("Total frames processed: " + str(count))      
        cv.imshow('frame',gray)
        count += 1
    else:
        print("Error reading frame!")
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Total frames processed: " + str(count))
        break
    
cap.release()
cv.destroyAllWindows()