import pytesseract as ocr
from threading import Thread
from PIL import Image
import cv2 as cv
import sys

class OcrThread(Thread):
    def __init__(self):
      Thread.__init__(self)

    def run(self, frame, result_queue):
      try:
        result = []
        result.append("../../images/" + frame.name)
        result.append(ocr.image_to_string(Image.fromarray(frame.image)))
        result_queue.put(result)
        print("ocr image processed: " + frame.name)
      except:
        print("Error:", sys.exc_info()[0])
        raise


    def create_ocr_thread(self, frame, result_queue):
        ocr = OcrThread()
        ocr.run(frame, result_queue)