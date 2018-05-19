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
    ocr = OcrThread()
    while True:
        if os.listdir("../../images") == []:
            print("Folder images is empty")
            already_processed.clear()
            time.sleep(.500)
        else:
            for file in os.listdir("../../images"):
                if not file in already_processed:
                    try:
                        print("start processing image: " + file)
                        imagem = cv.imread("../../images/" + file, cv.IMREAD_GRAYSCALE)
                        imgProcessing = ImageProcessing()
                        img = Frame(imagem, file, None, None)
                        img.image = imgProcessing.Billateral(img.image)
                        img.image = imgProcessing.Canny(img.image)
                        imgProcessing.FindPossiblePlates(img)
                        img.CropAllPlatesBorders()
                        if len(img.arrayOfPlates) > 1:
                            for plate in enumerate(img.arrayOfPlates):
                                ocr.create_ocr_thread(plate[1], result_ocr)
                        else:
                            result_ocr.put(["../../images/" + file, ""])
                        already_processed.append(file)
                        time.sleep(.100)
                    except:
                        print("Error:", sys.exc_info()[0])
                        raise

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
            gpio.output(21, gpio.HIGH)
            time.sleep(1)
            gpio.output(21, gpio.LOW)
        if not cam.remove(result[0]) == 0:
            print("An error ocurred when removing image " + result[0])
    else:
        print("No results returned yet")

cv.waitkey(0)