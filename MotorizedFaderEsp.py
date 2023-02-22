# Author: Simon Rödig

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
dc_frequency = 100
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
current_mode_arr = ["timeX", "timeX+1"]

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

def mode_changed(new_mode):
    
    if (new_mode == "off"):
        pi_in_bit0.value(0)
        pi_in_bit1.value(0)
        set_offline_slider()
    
    if (new_mode == "ap"):
        pi_in_bit0.value(0)
        pi_in_bit1.value(1)
        set_access_point_slider()
        
    if (new_mode == "ln"):
        pi_in_bit0.value(1)
        pi_in_bit1.value(0)
        set_local_network_slider()
            
    if (new_mode == "fi"):
        pi_in_bit0.value(1)
        pi_in_bit1.value(1)
        set_full_internet_slider()
        
    set_led(new_mode)

        
def check_mode():
    current_mode_arr.append(get_mode_from_raspi())
    current_mode_arr.pop(0)
    if (current_mode_arr[0] != current_mode_arr[1]):
        mode_changed(current_mode_arr[1])
    
    current_mode_arr.append(get_mode_from_slider())
    current_mode_arr.pop(0)
    if (current_mode_arr[0] != current_mode_arr[1]):
        print("Change on slider occurred")
        mode_changed(current_mode_arr[1])

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
    

while True:
    """
    # For Testing
    mode_changed("off")
    sleep(1)
    mode_changed("ap")
    sleep(1)
    mode_changed("ln")
    sleep(1)
    mode_changed("fi")
    sleep(1)
    """
    check_mode()
    sleep(0.25)
    
    

        

        
    
    
    
    
    
    
 

