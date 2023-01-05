class servo:
    def __init__(self):
         pass
      
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
