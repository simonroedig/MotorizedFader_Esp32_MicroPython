# Erlaubt benutzen vom Slider, led's leuchten dann

from machine import Pin, ADC, PWM
from time import sleep
from dcmotor import DCMotor

# -- Raspi_Output=Esp_Input 2-bit Communication -- #
pi_out_bit0 = Pin(23, Pin.IN)
pi_out_bit1 = Pin(22, Pin.IN)

# -- Raspi_Input=Esp_Output 2-bit Communication -- #
pi_in_bit0 = Pin(4, Pin.OUT)
pi_in_bit1 = Pin(0, Pin.OUT)

# -- Poti -- #
wiper = ADC(Pin(34))
wiper.atten(ADC.ATTN_11DB)
wiper.width(wiper.WIDTH_12BIT)

# -- LED's -- #
led_off = Pin(15, Pin.OUT) # red
led_ap = Pin(2, Pin.OUT) # yellow
led_ln = Pin(16, Pin.OUT) # blue
led_fi = Pin(17, Pin.OUT) # green

# -- DC-Motor -- #
# forward = down to off // backwards = up to full_internet
dc_frequency = 75
dc_speed = 100
dc_pin1 = Pin(32, Pin.OUT)    
dc_pin2 = Pin(33, Pin.OUT)     
enable = PWM(Pin(25), dc_frequency)
dc_motor = DCMotor(dc_pin1, dc_pin2, enable)

# -- Modes Poti Variables -- #
off = 4095
ap = 3000
ln = 1400
fi = 0

def set_led(mode):
    if (mode == "off"):
        led_off.value(1)
        led_ap.value(0)
        led_ln.value(0)
        led_fi.value(0)
        
    if (mode == "ap"):
        led_off.value(0)
        led_ap.value(1)
        led_ln.value(0)
        led_fi.value(0)
        
    if (mode == "ln"):
        led_off.value(0)
        led_ap.value(0)
        led_ln.value(1)
        led_fi.value(0)
        
    if (mode == "fi"):
        led_off.value(0)
        led_ap.value(0)
        led_ln.value(0)
        led_fi.value(1)
    

def get_mode_from_slider():
    # 00 = offline
    wiper_value = wiper.read()
    if ((wiper_value < off + off*10/100) and (wiper_value > off - off*10/100)):
        return "off"
        
    # 01 = access point
    if ((wiper_value < ap + ap*10/100) and (wiper_value > ap - ap*10/100)):
        return "ap"
        
    # 10 = local network
    if ((wiper_value < ln + ln*10/100) and (wiper_value > ln - ln*10/100)):
        return "ln"
    
    # 11 = full internet
    if ((wiper_value < fi + 200) and (wiper_value > fi - fi*10/100)):
        return "fi"


while True:
    set_led(get_mode_from_slider())
    

    



    
        

        
    
    
    
    
    
    
 


