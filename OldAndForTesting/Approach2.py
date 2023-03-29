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

def get_mode_from_slider_and_send_to_raspi():
    # 00 = offline
    wiper_value = wiper.read()
    if ((wiper_value < off + off*10/100) and (wiper_value > off - off*10/100)):
        pi_in_bit0.value(0)
        pi_in_bit1.value(0)
        return "off"
        
    # 01 = access point
    if ((wiper_value < ap + ap*10/100) and (wiper_value > ap - ap*10/100)):
        pi_in_bit0.value(0)
        pi_in_bit1.value(1)
        return "ap"
        
    # 10 = local network
    if ((wiper_value < ln + ln*10/100) and (wiper_value > ln - ln*10/100)):
        pi_in_bit0.value(1)
        pi_in_bit1.value(0)
        return "ln"
    
    # 11 = full internet
    if ((wiper_value < fi + fi*10/100) and (wiper_value > fi - fi*10/100)):
        pi_in_bit0.value(1)
        pi_in_bit1.value(1)
        return "fi"
    
def send_to_raspi(mode):
    if (mode == "off"):
        pi_in_bit0.value(0)
        pi_in_bit1.value(0)
    
    if (mode == "ap"):
        pi_in_bit0.value(0)
        pi_in_bit1.value(1)
        
    if (mode == "ln"):
        pi_in_bit0.value(1)
        pi_in_bit1.value(0)
            
    if (mode == "fi"):
        pi_in_bit0.value(1)
        pi_in_bit1.value(1)

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
    if ((wiper_value < fi + fi*10/100) and (wiper_value > fi - fi*10/100)):
        return "fi"

def get_mode_from_raspi():
    # 00 = offline
    if (pi_out_bit0.value() == 0 and pi_out_bit1.value() == 0):
        return "off"
        
    # 01 = access point
    if (pi_out_bit0.value() == 0 and pi_out_bit1.value() == 1):
        return "ap"
        
    # 10 = local network
    if (pi_out_bit0.value() == 1 and pi_out_bit1.value() == 0):
        return "ln"
    
    # 11 = full internet
    if (pi_out_bit0.value() == 1 and pi_out_bit1.value() == 1):
        return "fi"

def change_mode(new_mode):
    if (new_mode == "off"):
        set_offline_slider()
    
    if (new_mode == "ap"):
        set_access_point_slider()
        
    if (new_mode == "ln"):
        set_local_network_slider()
            
    if (new_mode == "fi"):
        set_full_internet_slider()

def set_full_internet_slider():
    wiper_value = wiper.read()
    print("FULL INTERNET")

    if ((wiper_value < fi + fi*10/100) and (wiper_value > fi - fi*10/100)):
        return
    while(wiper_value < fi):
        wiper_value = wiper.read()
        dc_motor.forward(dc_speed)
    while(wiper_value > fi):
        wiper_value = wiper.read()
        dc_motor.backwards(dc_speed)
        sleep(0.1)
    
    print("-> Wiper Value: " + str(wiper_value) + "\n")
    dc_motor.stop()
    
def set_local_network_slider():
    wiper_value = wiper.read()
    print("LOCAL NETWORK")

    if ((wiper_value < ln + ln*10/100) and (wiper_value > ln - ln*10/100)):
        return
    while(wiper_value < ln):
        wiper_value = wiper.read()
        dc_motor.forward(dc_speed)
    while(wiper_value > ln):
        wiper_value = wiper.read()
        dc_motor.backwards(dc_speed)
        
    print("-> Wiper Value: " + str(wiper_value) + "\n")
    dc_motor.stop()
    
def set_access_point_slider():
    wiper_value = wiper.read()
    print("ACCESS POINT")
    
    if ((wiper_value < ap + ap*10/100) and (wiper_value > ap - ap*10/100)):
        return
    while(wiper_value < ap):
        wiper_value = wiper.read()
        dc_motor.forward(dc_speed)
    while(wiper_value > ap):
        wiper_value = wiper.read()
        dc_motor.backwards(dc_speed)
    
    print("-> Wiper Value: " + str(wiper_value) + "\n")
    dc_motor.stop()
    
def set_offline_slider():
    wiper_value = wiper.read()
    print("OFFLINE")
    
    if (wiper_value == off):
        return
    if ((wiper_value < off + off*10/100) and (wiper_value > off - off*10/100)):
        dc_motor.forward(dc_speed)
    while(wiper_value < off):
        wiper_value = wiper.read()
        dc_motor.forward(dc_speed)
        sleep(0.2)
    while(wiper_value > off):
        wiper_value = wiper.read()
        dc_motor.backwards(dc_speed)
    
    print("-> Wiper Value: " + str(wiper_value) + "\n")
    dc_motor.stop()

pi_arr = ["timeX", "timeX+1"]
newFromPi = False

while True:
    f = get_mode_from_slider()
    set_led(f)
    
    sleep(0.01)

    pi = get_mode_from_raspi()
    pi_arr.append(pi)
    pi_arr.pop(0)
    if (pi_arr[0] != pi_arr[1]):
        newFromPi = True
    else:
        newFromPi = False

    slider = get_mode_from_slider()

    if ((pi != slider) and (slider == f) and newFromPi):
        set_led(change_mode(pi))
        send_to_raspi(pi)
        sleep(0.1)
    
    if ((pi != slider) and (slider == f) and not newFromPi):
        send_to_raspi(slider)



    
        

        
    
    
    
    
    
    
 

