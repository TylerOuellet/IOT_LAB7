import time
import ADC0832
import math
import RPi.GPIO as GPIO
import requests
import dweepy
import threading
dweetIO = "https://dweet.io/dweet/for/" 
myThing = "TO_RPI"

temp = "INIT"
distance = "INIT"

trig = 20
echo = 21
LED_PIN = 25

def listener():
     print("Thread_Loaded")
     for dweet in dweepy.listen_for_dweets_from(myThing):
        
        if "content" in dweet:
            if "Distance" in dweet["content"]:
                print("Distance: ",dweet["content"]["Distance"])
                collected_distance = dweet["content"]["Distance"]
                print(int(collected_distance))
                if float(collected_distance) > 1:
                    print("Distance Trigger!")
                    GPIO.output(LED_PIN,True)
                    time.sleep(2)
                    GPIO.output(LED_PIN,False)

listening_thread = threading.Thread(None, listener)
def init():
    ADC0832.setup()
    GPIO.setup(trig,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echo,GPIO.IN)
    GPIO.setup(LED_PIN,  GPIO.OUT)

def checkdist():
	GPIO.output(trig, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(trig, GPIO.LOW)
	while not GPIO.input(echo):
		pass
	t1 = time.time()
	while GPIO.input(echo):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

     

def loop():
    while True:
        res = ADC0832.getADC(0)
        if res == 0:
            temp = "N.A"
            continue
        Vr = 3.3 * float(res) / 255
        if Vr == 3.3:
            temp = "N.A"
            continue

       
        celciusTemp = float
        kelvenTemp = float

        kelvenTemp = 1/298.15 + 1/3455 * math.log((255 / res) - 1)

        kelvenTemp = 1/kelvenTemp
        celciusTemp = kelvenTemp - 273.15

        #Discard Garbage Values
        if celciusTemp >= 50 or celciusTemp<= -50:
            temp = "Discarded Value"
            print("Outlier, Descarded value")
        else:
            celciusTemp = round(celciusTemp,2)
            celciusTemp = str(celciusTemp)
            celciusTemp = celciusTemp
            temp = celciusTemp
        
        distance = checkdist()
        dweepy.dweet_for(myThing, {"Temperature": str(temp), "Distance": str(distance)})
        time.sleep(5)

if __name__ == '__main__':
    listening_thread.setDaemon(True)
    listening_thread.start()
    init()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.output(LED_PIN,False)
        ADC0832.destroy()
        print('The end!')