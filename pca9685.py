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
                    
                    # read in two bytes for moduleBase and moduleFunction
                    b = r.read(2)
                    
                    if len(b) < 2:
                        print("Error: no data")
                        continue
                        
                    # at this point the code should be clean.
                    #  we set the base and function here.
                    moduleBase = b[0]
                    moduleFunc = b[1]
                    
                    # 0x00 - Status 
                    if moduleBase == _STATUS_BASE:
                        # 0x01 - Hardware ID Code
                        if moduleFunc == _STATUS_HW_ID:
                            if DEBUG: print("hardware ID")
                            data[0] = _HW_ID_CODE
                  
                        elif moduleFunc == _STATUS_SWRST:
                            ## reset board, recieve 0xFF
                            b = r.read(1)
                            if b[0] == 0xFF:
                                print("restarting")
                            ## implement some kind of reset later.
                        
                    # 0x0D - EEPROM
                    elif moduleBase == _EEPROM_BASE:
                        # 0x3F or other
                        if moduleFunc == _EEPROM_I2C_ADDR: ## example pin
                            # TODO: implement set function
                            # b = read(1)
                            # if b:
                            #     reg[index][index] = b[0]
                            pass

                    # 0x09 - ADC
                    elif moduleBase == _ADC_BASE:
                        # TODO: implement moduleFunc 
                        pass

                    # 0x01 - GPIO
                    elif moduleBase == _GPIO_BASE:
                        
                        #
                        if moduleFunc == _GPIO_BULK:
                            #n = r.write(bytes([regs[index]]))
                            data = byte(32)
                            counter = 0

                            for pin in pins:
                                    data[counter] = pin.value
                                    counter += 1

                            #self.read(_GPIO_BASE, _GPIO_BULK, data)

                        elif moduleFunc == _GPIO_BULK_SET:
                            pass
                         
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
