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

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.OUT)

cam = Camera()
result_ocr = queue.Queue()

def image_name():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')

def handle_images():
    already_processed = []
    while True:
        if os.listdir("../../images") == []:
            print("Folder images is empty")
            already_processed.clear()
            time.sleep(.500)
        else:
            for file in os.listdir("../../images"):
                if not file in already_processed:
                    try:
                        print("started processing image: " + file)
                        imagem = cv.imread("../../images/" + file, cv.IMREAD_GRAYSCALE)
                        if imagem is not None:
                            imgProcessing = ImageProcessing()
                            img = Frame(imagem, file, None, None)
                            img.image = imgProcessing.Billateral(img.image)
                            img.image = imgProcessing.Canny(img.image)
                            imgProcessing.FindPossiblePlates(img)
                            img.CropAllPlatesBorders()
                            if len(img.arrayOfPlates) > 0:
                                for plate in enumerate(img.arrayOfPlates):
                                    ocr = OcrThread(plate[1], result_ocr)
                                    ocr.start()
                            else:
                                result_ocr.put(["../../images/" + file, ""])
                                print("Image: " + file + " Possible plates found: " + str(len(img.arrayOfPlates)))
                            already_processed.append(file)
                        else:
                            print("Error reading image " + file)
                            time.sleep(.100)
                    except:
                        print("Error: ", sys.exc_info()[0])

def open_gate():
    gpio.output(21, gpio.HIGH)
    time.sleep(1)
    gpio.output(21, gpio.LOW)

t = threading.Thread(target=handle_images)
t.start()

while True:
    cam.capture("640x480", str(image_name()), "jpg")
    time.sleep(.300)
    if not result_ocr.empty():
        result = result_ocr.get_nowait()
        print("Image returned: " + result[0])
        print("Image result: " + result[1])
        if not result[1] == "":
            open_gate()
        if not cam.remove(result[0]) == 0:
            print("An error ocurred when removing image " + result[0])
    else:
        print("No results returned yet")

cv.waitkey(0)
