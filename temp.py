import time
import subprocess

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import smbus
import Adafruit_SSD1306
import time
import os
import cv2
import numpy as np
#from camera import Camera
from loftr.utils.cvpr_ds_config import default_cfg
from utils import make_query_image, get_coarse_match, make_student_config
import nanocamera as nano



# 128x32 display and hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=0, gpio=1)# Set GPIO
# Initialize the library.
disp.begin()
# Clear display
disp.clear()
disp.display()
# Create a blank image for the drawing
# Make sure to create an image with the mode '1', i.e. 1-bit color
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Gets the drawing object to draw on the image
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes
# First, define some constants to make it easy to resize the shape
padding = -2
top = padding
bottom = height-padding
# Move left to right to track the current x position of the drawing.
x = 0
# Load default font
font = ImageFont.load_default()

def get_ip_address(args): # filler, TODO make this actual
    return '192.168.0.148'


img = Image.open("a.png")
img = img.resize((width, height))
print(np.array(img).shape, np.array(img).max())
img = img.convert('1')
print(np.array(img).shape, np.array(img).max())
disp.image(img)
disp.display()

#i = 0
#while True:
#    draw.rectangle((0,0,width,height), outline=0, fill=0)
#    draw.text((x, top), f"iran is the best {i}", font=font, fill=i)
#    disp.image(image)
#    disp.display()
#
#    time.sleep(0.01)
#    i = (i + 1) % 256


#while True:
#    # Draw a black filled box to clear the image.
#    draw.rectangle((0,0,width,height), outline=0, fill=0)
#    # You can get the shell script for system monitoring from this link:
#    #https://unix.stackexchange.com/questions/119126/command-to-display-memoryusage-disk-usage-and-cpu-load
#    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
#    CPU = subprocess.check_output(cmd, shell = True )
#    cmd = "free -m | awk 'NR==2{printf \"Mem:%s/%sM %.2f%%\", $3,$2,$3*100/$2}'"
#    MemUsage = subprocess.check_output(cmd, shell = True )
#    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk:%d/%dGB %s\", $3,$2,$5}'"
#    Disk = subprocess.check_output(cmd, shell = True )
#    draw.text((x, top), "eth0:" + str(get_ip_address('eth0')), font=font,
#    fill=255)
#    draw.text((x, top+8), "wlan0:" + str(get_ip_address('wlan0')),
#    font=font, fill=255)
#    draw.text((x, top+16), str(MemUsage.decode('utf-8')), font=font,
#    fill=255)
#    draw.text((x, top+25), str(Disk.decode('utf-8')), font=font, fill=255)
#    # Display image
#    disp.image(image)
#    disp.display()
#    time.sleep(1)