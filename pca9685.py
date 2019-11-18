## CircuitPython
##  An implementation of SeeSaw in CircuitPython
##
##
import board
import pulseio
import time
import digitalio
from i2cslave import I2CSlave


## Enable Debug Output
DEBUG = True

# template registers
regs = [0] * 255
index = 0
servos = []

# BASE REGISTER ADDRESSES
MODE1_BASE = 0x00
PRESCALE_BASE = 0xFE
PWM_BASE = 0x06
PWM_START_ADDRESS = []

for i in range(0, 15):
    # each LED is 4 bytes of register
    addr = PWM_BASE + (4 * i)
    PWM_START_ADDRESS.append(addr)

# setup servos - have to do manually because CircuitPython doesn't understand timer free
servo3 = pulseio.PWMOut(board.SERVO3, frequency=50, duty_cycle=2 ** 12)
servo1 = pulseio.PWMOut(board.SERVO1, frequency=50, duty_cycle=2 ** 12)
servo2 = pulseio.PWMOut(board.SERVO2, frequency=50, duty_cycle=2 ** 12)
servo4 = pulseio.PWMOut(board.SERVO4, frequency=50, duty_cycle=2 ** 12)
servo5 = pulseio.PWMOut(board.SERVO5, frequency=50, duty_cycle=2 ** 12)
servo6 = pulseio.PWMOut(board.SERVO6, frequency=50, duty_cycle=2 ** 12)
servo7 = pulseio.PWMOut(board.SERVO7, frequency=50, duty_cycle=2 ** 12)
servo8 = pulseio.PWMOut(board.SERVO8, frequency=50, duty_cycle=2 ** 12)

servos.append(servo1)
servos.append(servo2)
servos.append(servo3)
servos.append(servo4)
servos.append(servo5)
servos.append(servo6)
servos.append(servo7)
servos.append(servo8)

def read_register(base, size):
    ret = ""
    for i in range(0, size):
        ret = ret + "{:02x}".format(regs[base + i])

    print(ret)


# Data to send back on next i2cget command. 
# TODO: implement a proper register map

regs[MODE1_BASE] = 0b00000000
regs[PRESCALE_BASE] = 0b11111110


# I2C Device(s)
#    PCA9685 - 0x40
with I2CSlave(board.SCL, board.SDA, [0x40]) as slave:
    while True:
        r = slave.request()
        if not r:
            # Maybe do some housekeeping
            continue
        with r:  # Closes the transfer if necessary by sending a NACK or feeding the master dummy bytes
            if DEBUG: print("BEGIN request")
            
            if r.address == 0x40:
                # This is used by i2cset commands (or similar) and sets which register is next to be read from.
                if not r.is_read:  # Master write which is Slave read
                    if DEBUG: print("slave read")
                    
                    # read up to 5 bytes - one byte for register address
                    b = r.read(5)
                    
                    
                    if len(b) < 1:
                        print("Error: no data")
                        continue

                    moduleBase = b[0]
                    index = moduleBase

                    if DEBUG: print("base: 0x{:02x}".format(moduleBase))
                    print("all data: ", b)
                    for element in b:
                        print("0x{:02x}".format(element))
                    
                        
                    # We have a register address.  We need to decide what to do next.
                    if moduleBase == MODE1_BASE:
                        if len(b) < 2:
                            # could be combined transfer
                            if DEBUG: print("CT request")
                            continue

                        # set the mode1 register value
                        regs[moduleBase] = b[1]

                        # TODO: Action request - potentially in not r

                    elif moduleBase == PRESCALE_BASE:
                        if len(b) < 2:
                            # could be combined transfer
                            if DEBUG: print("CT request")
                            continue

                        # set the frequency
                        regs[moduleBase] = b[1]

                        # TODO:  Action request - potentially in not r
                    elif moduleBase in PWM_START_ADDRESS:
                        if len(b) < 5:
                            # could be combined transfer
                            if DEBUG: print("PWM: less than 5 bytes")
                            continue

                        # set registers
                        regs[moduleBase] = int(b[4])
                        regs[moduleBase + 1] = int(b[3])
                        regs[moduleBase + 2] = int(b[2])
                        regs[moduleBase + 3] = int(b[1])

                        

                        
                    
                                             
                # This is used by i2cget commands (or similar) and reads back the register that is set as 
                #  index.  No read transactions can take place in this section.  Works when given a register.
                elif r.is_restart:  # Combined transfer: This is the Master read message
                    if DEBUG: print("combined transfer")
                    #n = r.write(bytes([regs[index]]))
                    if DEBUG: print(regs[index])
                    n = r.write(bytes(regs[index]))
                
                # This is used by i2cget commands (or similar) and reads back the register that is set as 
                #  index.  No read transactions can take place in this section.  Works when no register given.
                else:  # A read transfer
                    if DEBUG: print("read transfer")
                    n = r.write(bytes(regs[index]))
                    # If the Master tries, it will get 0xff byte(s) by the ctx manager (r.close())
