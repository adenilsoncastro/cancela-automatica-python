import os
from subprocess import call
import subprocess

class Camera:
	def __init__(self):
		pass

	def capture(self, resolution, name, format):
		call(["fswebcam", "-r", resolution, "--no-banner", "../../images/" + name + "." + format])

	def remove(self, file):
		if os.path.isfile(file):
			os.remove(file)
			return 0
		else:
			return -1

	def findDevice(self):		
		devices = subprocess.run(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE)
		return_string = str(devices)
		splited = return_string.split("stdout=b")[1].split("\\n\\n")
		if "HP" in splited[0]:
			return 0

		if "HP" in splited[1]:
			return 1