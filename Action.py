# This class is responsible for the actions of the stepper motor.
# It has the methods to rotate the motor clockwise and counterclockwise,
# and to enable and disable the relay. It also has a method to verify the
# activation of the motor.

import machine
import time

class Action():
    
    def __init__(self, pin_dir, pin_step, pin_enable, revolution, pin_rele):
        self.pin_dir = machine.Pin(pin_dir, machine.Pin.OUT)
        self.pin_step = machine.Pin(pin_step, machine.Pin.OUT)
        self.pin_enable = machine.Pin(pin_enable, machine.Pin.OUT)
        self.pin_rele = machine.Pin(pin_rele, machine.Pin.OUT)
        self.revolution = revolution
        self.varify_master = False
    
    def VerifyActivation(self, activation):
        if str(activation) == 'True' and self.varify_master == False:
            self.varify_master = True
            return True
        else:
            return False

    def ClockwiseRotation(self):
        self.pin_dir.on()
        for i in range(0, self.revolution):
            self.pin_step.on()
            time.sleep_ms(1)
            self.pin_step.off()
            time.sleep_ms(1)
    
    def AnticlockwiseRotation(self):
        self.pin_dir.off()
        for i in range(0, self.revolution):
            self.pin_step.on()
            machine.time.sleep_ms(1)
            self.pin_step.off()
            machine.time.sleep_ms(1)

    def EnableRele(self):
        self.pin_rele.on()
        
    def DisableRele(self):
        self.pin_rele.off()