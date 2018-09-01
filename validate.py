import numpy as np
import cv2 as cv 
from PIL import Image
import pytesseract as ocr
import datetime
import time
import os
import sys
import RPi.GPIO as gpio
from RPLCD.gpio import CharLCD
import uuid
import shutil
from camera import Camera
from imageProcessing import ImageProcessing
from frame import Frame
from verificaPlaca import VerificaPlaca as vp
import platews as ws

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
    shutil.copyfile("correct.png", "../cancela-automatica-interface/image/correct.png")
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
        cv.imwrite("../processed/original/" + img.name + ".png", img.image)
        log("Start processing frame " + str(img.name) + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("Start processing frame " + str(img.name) + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        img.image = imgProcessing.Billateral(img.image)
        cv.imwrite("../processed/billateral/" + img.name + ".png", img.image)
        img.image = imgProcessing.Canny(img.image)
        cv.imwrite("../processed/canny/" + img.name + ".png", img.image)        
        imgProcessing.FindPossiblePlates(img)
        img.CropAllPlatesBorders()
        #img.validateAmountOfWhiteAndBlackPixels()        
        log("New frame " + str(img.name) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("New frame " + str(img.name) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))        
        if len(img.arrayOfPlates) > 0:
            log(str(len(img.arrayOfPlates)) + " possible plates found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
            print(str(len(img.arrayOfPlates)) + " possible plates found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
            for plate in img.arrayOfPlates:
                #_,otsu = imgProcessing.ThresholdPlusOtsu(plate.image, 90)
                #_,normal = imgProcessing.Threshold(plate.image, 105)
                #cv.imwrite("../processed/threshold_otsu/" + str(img.name) + ".png", otsu, 90)
                #cv.imwrite("../processed/threshold_normal/" + str(img.name) + ".png", normal, 105)

                _,plate.image = imgProcessing.ThresholdPlusOtsu(plate.image, 105)
                #_,plate.image = cv.threshold(plate.image,105,255,0)
                cv.imwrite("../processed/" + str(image_name()) + ".png", plate.image)
                result = ocr.image_to_string(Image.fromarray(plate.image), config="--psm 8")
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
            log("No plates found, applying dilate filter...")
            print("No plates found, applying dilate filter...")
            img.image = imgProcessing.Dilate(img.image)
            cv.imwrite("../processed/dilate/" + str(img.name) + " .png", img.image)
            imgProcessing.FindPossiblePlates(img)
            if len(img.arrayOfPlates) >  0:
                log(str(len(img.arrayOfPlates)) + " possible plate found after applying dilate filter")
                print(str(len(img.arrayOfPlates)) + " possible plate found after applying dilate filter")
                for plate in img.arrayOfPlates:
                    _,plate.image = cv.threshold(plate.image,105,255,0)
                    cv.imwrite("../processed/" + str(image_name()) + ".png", plate.image)
                    result = ocr.image_to_string(Image.fromarray(plate.image), config="--psm 8")
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
                log("No plates found after applying dilate")
                print("No plates found after applying dilate")
        print("Total frames processed: " + str(count))      
        #cv.imshow('frame',gray)
        count += 1
    else:
        print("Error reading frame!")
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Total frames processed: " + str(count))
        break
    
cap.release()
cv.destroyAllWindows()