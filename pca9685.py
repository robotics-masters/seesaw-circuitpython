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

## SEESAW REGISTER MAP
seesawRegs = [0] * 16 # base registers

for reg in seesawRegs:
    reg = [0] * 16


# template registers
regs = [0] * 16
index = 0

# Data to send back on next i2cget command. 
# TODO: implement a proper register map
data = [0] * 16

led = pulseio.PWMOut(board.SERVO1, frequency=5000, duty_cycle=0)

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
                    
                    # read in one byte
                    b = r.read(1)
                    
                    if len(b) < 1:
                        print("Error: no data")
                        continue
                        
                    # at this point the code should be clean.
                    #  we set the base and function here.
                    moduleBase = b[0]
                    
                                             
                # This is used by i2cget commands (or similar) and reads back the register that is set as 
                #  index.  No read transactions can take place in this section.  Works when given a register.
                elif r.is_restart:  # Combined transfer: This is the Master read message
                    if DEBUG: print("combined transfer")
                    #n = r.write(bytes([regs[index]]))
                    if DEBUG: print(data)
                    n = r.write(bytes(data))
                
                # This is used by i2cget commands (or similar) and reads back the register that is set as 
                #  index.  No read transactions can take place in this section.  Works when no register given.
                else:  # A read transfer
                    if DEBUG: print("read transfer")
                    n = r.write(bytes(data))
                    # If the Master tries, it will get 0xff byte(s) by the ctx manager (r.close())
