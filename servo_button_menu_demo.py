import pickle
import os
import schedule # Schedule Library imported
import time
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
from RPi import GPIO
from servo import *
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

#Assiging pin numbers to buttons
button1=17
button2=18
button3=23

#Assiging pin number to servo
servopin = 12

#Assiging variables
global menuindex
global insubmenu
global weight
global spintime

#Setting up the buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Setting up the buttons
GPIO.setup(servopin, GPIO.OUT)

# GPIO 12 for PWM with 50Hz
p = GPIO.PWM(servopin, 50)
# Initialization
p.start(0) 

# Create an object hx which represents your real hx711 chip
# Required input parameters are only 'dout_pin' and 'pd_sck_pin'
hx = HX711(dout_pin=5, pd_sck_pin=6)

#Connecting to the OLED SSD1306
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

# getter method
def get_spintime(self):
    return self._spintime
      
# setter method
def set_spintime(self, spintime):
    self._spintime = spintime

# set angle
def setAngle(angle):
    duty = angle / 18 + 2
    
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(duty)
    
# spin method
def spin():
    count = 0

    if(get_spintime == 20):
        while(count < 4):
            print("set to 90-deg four times")
            setAngle(90)
            sleep(1)
            count=count+1
            
    if(get_spintime == 25):
        while(count < 6):
            print("set to 90-deg six times")
            setAngle(0)
            sleep(1)
            count=count+1
            
    if(get_spintime == 30):
        while(count < 8):
            print("set to 0-deg eight times")
            setAngle(0)
            sleep(1)
            count=count+1
            
def measure_weight():
    global weight
    
    try:
        # Check if we have swap file. If yes that suggest that the program was not
        # terminated proprly (power failure). We load the latest state.
        swap_file_name = 'swap_file.swp'
        if os.path.isfile(swap_file_name):
            with open(swap_file_name, 'rb') as swap_file:
                hx = pickle.load(swap_file)
                # now we loaded the state before the Pi restarted.
                
        # Read data several times and return mean value
      #  print(hx.get_weight_mean(20), 'g')
        weight = str("%.2f" % (hx.get_weight_mean(20)))
        print(weight)
        return (weight)
    except (KeyboardInterrupt, SystemExit):
        print('Bye :)')
        GPIO.cleanup()

    
#Outline of Display
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

# Sub 1 Menu operation
def sub_menu1_operation():
        while(1):
            sleep(0.50)
            if (GPIO.input(button1)==0):
                print("Option 20g Selected")
                spintime = 20
                set_spintime(spintime)
                with canvas(device) as draw:
                    draw.text((0, 20), "Option 20g Selected", fill="white")
                sleep(1)    
                break

            if (GPIO.input(button2)==0):
                print("Option 25g Selected")
                spintime = 25
                set_spintime(spintime)
                with canvas(device) as draw:
                    draw.text((0, 20), "Option 25g Selected", fill="white")  
                sleep(1)   
                break

            if (GPIO.input(button3)==0):
                print("Option 30g Selected")
                spintime = 30
                set_spintime(spintime)
                with canvas(device) as draw:
                    draw.text((0, 20), "Option 30g Selected", fill="white")
                sleep(1)
                break
            
# Sub 2 Menu operation
def sub_menu2_operation():
        while(1):
            sleep(0.50)
            if (GPIO.input(button1)==0):
                print("Option 3 Hr Selected")
                with canvas(device) as draw:
                    draw.text((0, 20), "Option 3 Hr Selected", fill="white")
##                    schedule.every(3).hours.do(geeks)
                    schedule.every(0.2).minutes.do(spin)
                sleep(1)    
                break

            if (GPIO.input(button2)==0):
                print("Option 3.5 Hr Selected")
                with canvas(device) as draw:
                    
                    draw.text((0, 20), "Option 3.5 Hr Selected", fill="white")
##                    schedule.every(3.5).hours.do(geeks)
                    schedule.every(0.5).minutes.do(spin)
                sleep(1)   
                break

            if (GPIO.input(button3)==0):
                print("Option 4 Hr Selected")
                with canvas(device) as draw:
                    draw.text((0, 20), "Option 4 Hr Selected", fill="white")
##                      schedule.every(4).hours.do(geeks)
                    schedule.every(0.6).minutes.do(spin)
                sleep(1)
                break            
            
# Main Menu operation	
def menu_operation():
    while(True):
        sleep(0.01)
        if (GPIO.input(button1)==0):
            sub_1 = ['[1] 20g', '[2] 25g', '[3] 30g']
            with canvas(device) as draw:
                menu(device, draw, sub_1, 1)
            sub_menu1_operation()
            sleep(1)    
            break

        if (GPIO.input(button2)==0):
            sub_2 = ['[1] 3 Hr', '[2] 3.5 Hr', '[3] 4 Hr']
            with canvas(device) as draw:
                menu(device, draw, sub_2, 1)
            sub_menu2_operation()
            sleep(1)    
            break    

        if (GPIO.input(button3)==0):
            measure_weight()
            with canvas(device) as draw:
                draw.text((0, 10), "Amount of food left: ", fill="white")
                draw.text((0, 20), weight, fill="white")
                draw.text((0, 30), "Next meal time: ", fill="white")
                draw.text((0, 40), "00:23", fill="white")
            sleep(1)    
            break     
                    
#MainScript
def main():
    try: 
        head = ("Automated Pet Food Dispenser program is running... ")
        print(head)
        device.clear()
        while True:
            names = ['1.) Quantity', '2.) Meals Freqeuncy', '3.) Information']
            with canvas(device) as draw:
                menu(device, draw, names, 0)
            schedule.run_pending()   
            menu_operation()
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nGPIO cleaned")
        print("\nProgram is stopped")
        
if __name__ == "__main__":
    main()
