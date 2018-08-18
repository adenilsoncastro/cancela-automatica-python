import pytesseract as ocr
from threading import Thread
from PIL import Image
import cv2 as cv
import sys
import datetime

def log(text):
    with open("log.txt","a") as file:
        file.write(text + "\n")

class OcrThread(Thread):
    def __init__(self, frame, result_queue):
      Thread.__init__(self)
      self.frame = frame
      self.result_queue = result_queue

    def run(self):
      try:
        result = []
        result.append("../../images/" + self.frame.name)
        result.append(ocr.image_to_string(Image.fromarray(self.frame.image),config="--psm 8"))
        self.result_queue.put(result)
        print("ocr image processed: " + self.frame.name)
        log("ocr image processed: " + self.frame.name + " at " + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f'))
      except:
        print("OCR Error:", sys.exc_info()[0])
        raise

    def create_ocr_thread(self, frame, result_queue):
        ocr = OcrThread(frame, result_queue)
        ocr.run(frame, result_queue)