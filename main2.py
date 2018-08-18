from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv
import numpy as np
from camera import Camera
from ocr import OcrThread
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

cam = Camera()
result_ocr = queue.Queue()
lcd = CharLCD(pin_rs=18, pin_e=23, pins_data=[26,19,13,6], numbering_mode=gpio.BCM, cols=16, rows=2)
allowCapture = True
threadList = []

def image_name():
    return str(uuid.uuid4()).split('-')[0]

def handle_images():
    already_processed = []
    while True:
        if os.listdir("../../images") == []:
            print("Folder images is empty")
            already_processed.clear()
            time.sleep(.100)
        else:
            for file in os.listdir("../../images"):
                if not file in already_processed:
                    try:
                        log("Start processing image " + file + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
                        imagem = cv.imread("../../images/" + file, cv.IMREAD_GRAYSCALE)
                        if imagem is not None:
                            cv.imwrite(os.path.join("../../", file + '_original.jpg'), imagem)
                            imgProcessing = ImageProcessing()
                            img = Frame(imagem, file, None, None)
                            img.image = imgProcessing.EqualizeHistogram(img.image)
                            img.image = imgProcessing.Billateral(img.image)
                            img.image = imgProcessing.Canny(img.image)
                            img.image = imgProcessing.GaussianBlur(img.image)
                            imgProcessing.FindPossiblePlates(img)
                            img.CropAllPlatesBorders()
                            if len(img.arrayOfPlates) > 0:
                                for plate in enumerate(img.arrayOfPlates):
                                    #_,plate[1].image = cv.threshold(plate[1].image, 105, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
                                    _,plate[1].image = imgProcessing.ThresholdPlusOtsu(plate[1].image, 105)
                                    ocr = OcrThread(plate[1], result_ocr)
                                    ocr.setName(uuid.uuid4())
                                    threadList.append(ocr.getName())
                                    log("New OCR thread created with id " + ocr.getName())
                                    ocr.start()
                                    log("Image " + file + " processed and sent to OCR at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f') + " with " + str(len(img.arrayOfPlates)) + " possible plate(s)")
                                img.SaveImage()
                                gpio.output(20, gpio.HIGH)
                                time.sleep(.250)
                                gpio.output(20, gpio.LOW)
                            else:
                                log("No plates found, applying dilate filter...")
                                img.image = imgProcessing.Dilate(img.image)
                                imgProcessing.FindPossiblePlates(img)
                                if len(img.arrayOfPlates) >  0:
                                    log(str(len(img.arrayOfPlates)) + " possible plate found after dilate filter")
                                    _,plate[1].image = cv.threshold(plate[1].image, 105, 255, cv.THRESH_BINARY)
                                    ocr = OcrThread(plate[1], result_ocr)
                                    ocr.start()
                                    log("Image " + file + " processed and sent to OCR at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f') + " with " + str(len(img.arrayOfPlates)) + " possible plate(s)")
                                    img.SaveImage()
                                    gpio.output(20, gpio.HIGH)
                                    time.sleep(.250)
                                    gpio.output(20, gpio.LOW)
                                else:
                                    log("No plates found after applying dilate")                                
                                    log("Image " + file + " processed with 0 possible plate(s) found at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
                                    if not cam.remove("../../images/" + file) == 0:
                                        log("An error ocurred when removing image " + file)
                                    else:
                                        log("Image " + file + " sucessfully removed")
                                    img.SaveImage()
                                    gpio.output(16, gpio.HIGH)
                                    time.sleep(.250)
                                    gpio.output(16, gpio.LOW)
                            already_processed.append(file)
                        else:
                            log("Error reading " + file)
                            time.sleep(.100)
                    except:
                        print("Error: ", sys.exc_info()[0])
                        log(str(sys.exc_info()[0]))

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
    lcd.write_string(name.split('/')[3])
    time.sleep(5)
    clean_data()
    allowCapture = True

def clean_data():
    for file in os.listdir("../../images"):
        try:
            os.remove(file)            
        except:
            print("Error: ", sys.exc_info()[0])
            log(str(sys.exc_info()[0]))
    log("Threads currently running: " + str(threading.enumerate()))
        

def log(text):
    with open("log.txt","a") as file:
        file.write(text + "\n")

def capture_images():
    while True:
        if allowCapture == True:
            cam.capture("1920x1080", str(image_name()), "jpg")
            time.sleep(.300)
        else:
            log("Image capture paused by system")
            time.sleep(.500)

t = threading.Thread(target=handle_images)
t.setName("Handle_images_thread")
t2 = threading.Thread(target=capture_images)
t2.setName("Capture_images_thread")
t.start()
t2.start()

while True:    
    if not result_ocr.empty():
        result = result_ocr.get_nowait()
        log("Image " + result[0] + " returned from OCR at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
        log("Image " + result[0] + " result: " + result[1])
        log("There is " + str(result_ocr.qsize()) + " itens in the queue")
        if not result[1] == "":
            open_gate(result[0],result[1])
        if not cam.remove(result[0]) == 0:
            log("An error ocurred when removing image " + result[0])
        else:
            log("Image " + result[0] + " successfully removed")       
    else:
        print("No results returned yet")
    time.sleep(.250)
cv.waitkey(0)
