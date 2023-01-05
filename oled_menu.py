from PIL import ImageFont
from time import sleep
from RPi import GPIO
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
GPIO.setmode(GPIO.BCM)

global menuindex
global insubmenu

L1 = 17
L2 = 27
L3 = 22
L4 = 10

C1 = 9
C2 = 11
C3 = 26

GPIO.setwarnings(False)            

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
             
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

def invert(draw,x,y,text):
    font = ImageFont.load_default()
    draw.rectangle((x, y, x+120, y+10), outline=255, fill=255)
    draw.text((x, y), text, font=font, outline=0,fill="black")
	
# Box and text rendered in portrait mode
def menu(device, draw, menustr,index):
    global menuindex
    font = ImageFont.load_default()
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    for i in range(len(menustr)):
        if(i == index):
            menuindex = i
            invert(draw, 2, i*10, menustr[i])
        else:
            draw.text((2, i*10), menustr[i], font=font, fill=255)		
		
names = ['1.) Quantity', '2.) Freqeuncy', '3.) Information']
with canvas(device) as draw:
    menu(device, draw, names, 1)
#
try:
    while(1):
        GPIO.output(GPIO.HIGH)
        if (GPIO.input(C1)==1) :
            with canvas(device) as draw:
                draw.text((0, 0), "Select quantity of next meal: ", fill="white")
                sleep(0.5)
                continue
                #draw.text((0, 26), sys_info.disk_usage('/'), fill="white")
        elif (GPIO.input(C2)==1):
            with canvas(device) as draw:
                draw.text((0, 0), "Select time before next meal: ", fill="white")
                sleep(0.5)
                continue
                #draw.text((0, 26), sys_info.mem_usage(), fill="white")
        elif (GPIO.input(C3)==1):
            with canvas(device) as draw:
                draw.text((0, 0), "Amount of kibble left: ", fill="white")
                draw.text((0, 0), "Time before next meal: ", fill="white")
                sleep(0.5)
                continue
                #draw.text((0, 26), sys_info.network('wlan0'), fill="white")
            
        names = ['1.) Quantity', '2.) Freqeuncy', '3.) Information']
        with canvas(device) as draw:
            menu(device, draw, names, 1)

except KeyboardInterrupt:
    GPIO.cleanup()

