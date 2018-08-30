import numpy as np
import cv2 as cv 
from PIL import Image
from camera import Camera
from ocr import OcrThread
import pytesseract as ocr
from imageProcessing import ImageProcessing
from frame import Frame
from verificaPlaca import VerificaPlaca as vp
import platews as ws
import queue
import datetime
import time
import os
import threading
import sys
import RPi.GPIO as gpio
from RPLCD.gpio import CharLCD
import uuid

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.OUT)
gpio.setup(20, gpio.OUT)
gpio.setup(16, gpio.OUT)

result_ocr = queue.Queue()
lcd = CharLCD(pin_rs=18, pin_e=23, pins_data=[26,19,13,6], numbering_mode=gpio.BCM, cols=16, rows=2)
allowCapture = True

cap = cv.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 720)
count = 0

def image_name():
    return str(uuid.uuid4()).split('-')[0]

def clean_data():
    for file in os.listdir("../../images"):
        try:
            os.remove("../../images/" + file)            
            log("clean_data removed image" + file)            
        except:
            print("Error: ", sys.exc_info())
            log("Error: " + str(sys.exc_info()) + " when removing ../../images/" + file)   

def open_gate(name,plate):
    allowCapture = False
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
    clean_data()
    allowCapture = True

def log(text):
    with open("log.txt","a+") as file:
        file.write(text + "\n")
        file.close()

imgProcessing = ImageProcessing()
verificaPlaca = vp()

def result():
    while True:
        if not result_ocr.empty():
            result = result_ocr.get_nowait()
            log("OCR processed frame " + result[0] + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f') + " RESULT:" + result[1])
            open_gate(result[0],result[1])
        time.sleep(.1)

#t = threading.Thread(target=result)
#t.start()

log("entering program loop...")
while(True):    
    for i in range(4):
        cap.grab()
    ret, frame = cap.read()
    if ret == True:
        log("new frame captured at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("new frame captured at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    
        img = Frame(np.array(Image.fromarray(gray)), str(image_name()), None, None)
        img.image = imgProcessing.Billateral(img.image)
        img.image = imgProcessing.Canny(img.image)
        img.image = imgProcessing.GaussianBlur(img.image)
        imgProcessing.FindPossiblePlates(img)
        img.CropAllPlatesBorders()
        #img.validateAmountOfWhiteAndBlackPixels()        
        log("new frame " + str(img.name) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("new frame " + str(img.name) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        if len(img.arrayOfPlates) > 0:
            log(str(len(img.arrayOfPlates)) + " possible plates found")
            print(str(len(img.arrayOfPlates)) + " possible plates found " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
            for plate in enumerate(img.arrayOfPlates):
                _,plate[1].image = imgProcessing.ThresholdPlusOtsu(plate[1].image, 105)
                #cv.imshow(str(image_name()), plate[1].image)
                cv.imwrite("../processed/" + str(image_name()) + ".png", plate[1].image)
                #log("Creating OCR Thread for frame " + str(img.name) + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')) 
                #x = OcrThread(plate[1], result_ocr)
                #x.start()
                result = ocr.image_to_string(Image.fromarray(plate[1].image),config="--psm 8")
                log("OCR FINISHED FOR FRAME " + str(img.name) + ". Result: " + result + " - TIME: " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))            
                print("OCR result: " + result)                
                placa = verificaPlaca.verificar(result)
                print("VP result: " + str(placa))
                if not placa == -1:          
                    #api = ws.checkForPlateExistence(placa)
                    #if api == True:
                    #   print("RETURN API")
                    #   open_gate(str(img.name),placa)
                    #   break
                    open_gate(str(img.name),placa)
                else:
                    print("Plate not recognized")
                    log("Plate not recongnized")
        else:
            print("Total frames processed: " + str(count))      
        cv.imshow('frame',gray)
        #cv.imwrite("frame%d.jpg" %count,gray)
        count += 1
    else:
        print("Erro reading frame!")
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Total frames processed: " + str(count))
        break
    
cap.release()
cv.destroyAllWindows()