import time
import ADC0832
import math
import RPi.GPIO as GPIO
import requests

dweetIO = "https://dweet.io/dweet/for/" 
myThing = "TO_RPI"

temp = "INIT"
distance = "INIT"

trig = 20
echo = 21

def init():
    ADC0832.setup()
    GPIO.setup(trig,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(echo,GPIO.IN)

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
        rqsString = dweetIO + myThing + '?' + 'temperature=' + str(temp) + '&' + 'distance=' + str(distance)
        print(rqsString)  # URL for post
        requests.post(rqsString)
        time.sleep(5)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print('The end!')