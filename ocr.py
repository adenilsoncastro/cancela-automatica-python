import pytesseract as ocr
from threading import Thread
from PIL import Image

class OcrThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self, image, result_queue):
        result_queue.put(ocr.image_to_string(image))

    def create_ocr_thread(self, image, result_queue):
        ocr = OcrThread()
        ocr.run(image, result_queue)