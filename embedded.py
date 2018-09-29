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
gpio.setup(21, gpio.OUT)#M1
gpio.setup(20, gpio.OUT)#led
gpio.setup(16, gpio.OUT)#M2
gpio.setup(24, gpio.IN)#Sensor barreira
gpio.setup(25, gpio.IN, pull_up_down = gpio.PUD_DOWN)#Fim de curso superior
gpio.setup(8, gpio.IN, pull_up_down = gpio.PUD_DOWN)#Fim de curso inferior

lcd = CharLCD(pin_rs=18, pin_e=23, pins_data=[26,19,13,6], numbering_mode=gpio.BCM, cols=16, rows=2)

cam = Camera()
print("HP Camera is in /dev/video" + str(cam.findDevice()))
cap = cv.VideoCapture(cam.findDevice())
cap.set(3, 1080)
cap.set(4, 720)
count = 0

if cam.findDevice() == 0:
    os.popen('zbarcam /dev/video1 > qr_result.txt')
else:
    os.popen('zbarcam /dev/video0 > qr_result.txt')

def image_name():
    return str(uuid.uuid4()).split('-')[0]

def qrcode():
    try:
        file = open("qr_result.txt", "r+")

        data = file.readlines()
        if data == []:
           print("No information available from QRCODE")
        else:
            result = data[0].split(":")
            print("QRCODE: \n" + str(result[1]) + "\n")
            id = result[1].rstrip()
            api = ws.checkForIdExistence(id)
            if api == True:
                open_gate("qrcode",id)
            #open_gate(str(plate._id),placa)
            else:
                update_screen("error")
                print("Id não reconhecido!")
                gpio.output(20, gpio.HIGH)
                time.sleep(.250)
                gpio.output(20, gpio.LOW)       
            time.sleep(2)
            file.truncate(0)
        file.close()
    except:
        print("Error: " + str(sys.exc_info()) + " when reading qrcode info")  

def open_gate(name,plate):
    cap.release()
    update_screen("correct")
    #gpio.output(21, gpio.HIGH)
    #time.sleep(.250)
    #gpio.output(21, gpio.LOW)
    #lcd.clear()
    #lcd.cursor_pos=(0,0)
    #lcd.write_string("Placa:")
    #lcd.write_string(plate)
    #lcd.cursor_pos=(1,0)
    #lcd.write_string(name)
    #time.sleep(5)
    while gpio.input(25) == gpio.LOW:
        gpio.output(21, gpio.HIGH)
        print("Cancela abrindo...")
    gpio.output(21, gpio.LOW)
    while gpio.input(25) == gpio.HIGH and gpio.input(24) == gpio.LOW:
        gpio.output(21, gpio.LOW)
        gpio.output(20, gpio.HIGH)
        time.sleep(.1)
        gpio.output(20, gpio.LOW)
        time.sleep(.1)
        print("Cancela aberta, aguardando passagem do veículo!")
    time.sleep(3)
    while gpio.input(8) == gpio.LOW:
        while gpio.input(8) == gpio.LOW and gpio.input(24) == gpio.LOW:
            gpio.output(16, gpio.HIGH)
            print("Cancela fechando")
        while gpio.input(8) == gpio.LOW and gpio.input(24) == gpio.HIGH:
            gpio.output(16, gpio.LOW)
            print("Obstáculo detectado!")
    gpio.output(16, gpio.LOW)
    time.sleep(2)  

    print("Cancela fechada!")    
    gpio.output(20, gpio.HIGH)    
    time.sleep(5)
    gpio.output(20, gpio.LOW)

    gpio.output(21, gpio.LOW)
    cap.open(cam.findDevice())
    cap.set(3, 1080)
    cap.set(4, 720)

def update_screen(image):
    path = "../cancela-automatica-interface/image/"
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    if len(files) > 0:
        if image == "correct":
            for f in files:
                try:
                    os.remove(path + f)
                    shutil.copyfile("correct.png", path + "correct.png")
                    log("Screen image updated sucessfully")
                except:
                    log("Error: " + str(sys.exc_info()) + " when updating screen image")
        elif image == "error":
            for f in files:
                try:
                    os.remove(path + f)
                    shutil.copyfile("error.png", path + "error.png")
                    log("Screen image updated sucessfully")
                except:
                    log("Error: " + str(sys.exc_info()) + " when updating screen image")
    else:
        if image == "correct":            
            try:
                shutil.copyfile("correct.png", path + "correct.png")
                log("Screen image updated sucessfully")
            except:
                log("Error: " + str(sys.exc_info()) + " when updating screen image")
        elif image == "error":
            try:
                shutil.copyfile("error.png", path + "error.png")
                log("Screen image updated sucessfully")
            except:
                log("Error: " + str(sys.exc_info()) + " when updating screen image")

def log(text):
    with open("log.txt","a+") as file:
        file.write(text + "\n")
        file.close()

def move_log():
    try:
        shutil.copyfile("log.txt", "logs/log_" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')) + ".txt")
        os.remove("log.txt")
    except:
        print("Error: " + str(sys.exc_info()))

imgProcessing = ImageProcessing()
verificaPlaca = vp() 
move_log()

while(True): 
    ret, frame = cap.read()
    if ret == True:
        log("New frame captured at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)        
        
        img = Frame(np.array(Image.fromarray(gray)), str(image_name()), None, None)
        cv.imwrite("../processed/original/" + img._id + ".png", img.image)
        log("Start processing frame " + str(img._id)+ " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("Start processing frame " + str(img._id) + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))

        img.CropImage()
        img.image = imgProcessing.Billateral(img.image)
        cv.imwrite("../processed/billateral/" + img._id + ".png", img.image)
        
        img.image = imgProcessing.Canny(img.image)
        cv.imwrite("../processed/canny/" + img._id + ".png", img.image)        
        
        imgProcessing.FindPossiblePlates(img, False, False)   
        log("New frame " + str(img._id) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        print("New frame " + str(img._id) + " finished processing at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))        

        if len(img.arrayOfPlates) == 0:
            log("No plates found in frame " + str(img._id) + ", applying dilate filter...")
            print("No plates found in frame " + str(img._id) + ", applying dilate filter...")
            img.image = imgProcessing.Dilate(img.image)
            cv.imwrite("../processed/dilate/" + str(img._id) + " .png", img.image)
            imgProcessing.FindPossiblePlates(img, False, True)
            if len(img.arrayOfPlates) == 0:
                log("No plates found in frame " + str(img._id) + ", after applying dilate filter.Trying GaussianBlur...")
                print("No plates found in frame " + str(img._id) + ", after applying dilate filter.Trying GaussianBlur...")
                img.image = imgProcessing.GaussianBlur(img.image)
                imgProcessing.FindPossiblePlates(img, False, True)
        
        if len(img.arrayOfPlates) == 0:
            log("No plates found without more light in frame " + str(img._id) + ", applying bright filter...")
            print("No plates found without more light in frame " + str(img._id) + ", applying bright filter...")
            
            img.image = imgProcessing.MoreLight(img.originalImage)
            img.image = imgProcessing.Billateral(img.image)
            img.image = imgProcessing.Canny(img.image)
            imgProcessing.FindPossiblePlates(img, True, False)

            if len(img.arrayOfPlates) == 0:
                log("No plates found in frame " + str(img._id) + " after MoreLight filter. Applying dilate filter...")
                print("No plates found in frame " + str(img._id) + " after MoreLight filter. Applying dilate filter...")
                img.image = imgProcessing.Dilate(img.image)
                cv.imwrite("../processed/dilate/" + str(img._id) + " .png", img.image)
                imgProcessing.FindPossiblePlates(img, True, True)
                if len(img.arrayOfPlates) == 0:
                    log("No plates found in frame " + str(img._id) + ", after applying dilate filter.Trying GaussianBlur...")
                    print("No plates found in frame " + str(img._id) + ", after applying dilate filter.Trying GaussianBlur...")
                    img.image = imgProcessing.GaussianBlur(img.image)
                    imgProcessing.FindPossiblePlates(img, True, True)

        img.CropAllPlatesBorders()
        img.validateAmountOfWhiteAndBlackPixels()

        if len(img.arrayOfPlates) > 0:
            log(str(len(img.arrayOfPlates)) + " possible plates found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f') + " in frame " + str(img._id))
            print(str(len(img.arrayOfPlates)) + " possible plates found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f') + " in frame " + str(img._id))
            for plate in img.arrayOfPlates:
                cv.imwrite("../processed/" + str(img._id) + ".png", plate.image)
                try:
                    result = ocr.image_to_string(Image.fromarray(plate.image), config="--psm 8")
                    log("OCR finished processing for frame " + str(plate._id) + ". Result: " + result + " - Time: " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))            
                    print("OCR result: " + result)                
                    placa = verificaPlaca.verificar(result)
                    log("VP result: " + str(placa))
                    print("VP result: " + str(placa))
                    if not placa == -1:          
                        #api = ws.checkForPlateExistence(placa)
                        #if api == True:
                        #   open_gate(str(plate._id),placa)
                        #else:
                        #    update_screen("error")
                        open_gate(str(plate._id),placa)
                    else:
                        update_screen("error")
                        gpio.output(20, gpio.HIGH)
                        time.sleep(.250)
                        gpio.output(20, gpio.LOW)
                        print("Plate not recognized")
                        log("Plate not recongnized")
                except:
                    log("Error: " + str(sys.exc_info()) + " when reading plate info from frame " + str(plate._id))
                    print("Error: " + str(sys.exc_info()) + " when reading plate info from frame " + str(plate._id))
        else:
            log("Sorry, no plates were found in frame " + str(img._id))
            print("Sorry, no plates were found in frame " + str(img._id))
                    
        print("Total frames processed: " + str(count))      
        #cv.imshow('frame',gray)
        count += 1
    else:
        print("Error reading frame!")
    
    qrcode()
    
cap.release()
cv.destroyAllWindows()