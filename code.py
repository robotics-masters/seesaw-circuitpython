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



## DEFAULT CONFIG (similar to seesaw board_config.h)


_STATUS_BASE = const(0x00)

_GPIO_BASE = const(0x01)
_SERCOM0_BASE = const(0x02)

_TIMER_BASE = const(0x08)
_ADC_BASE = const(0x09)
_DAC_BASE = const(0x0A)
_INTERRUPT_BASE = const(0x0B)
_DAP_BASE = const(0x0C)
_EEPROM_BASE = const(0x0D)
_NEOPIXEL_BASE = const(0x0E)
_TOUCH_BASE = const(0x0F)

_GPIO_DIRSET_BULK = const(0x02)
_GPIO_DIRCLR_BULK = const(0x03)
_GPIO_BULK = const(0x04)
_GPIO_BULK_SET = const(0x05)
_GPIO_BULK_CLR = const(0x06)
_GPIO_BULK_TOGGLE = const(0x07)
_GPIO_INTENSET = const(0x08)
_GPIO_INTENCLR = const(0x09)
_GPIO_INTFLAG = const(0x0A)
_GPIO_PULLENSET = const(0x0B)
_GPIO_PULLENCLR = const(0x0C)

_STATUS_HW_ID = const(0x01)
_STATUS_VERSION = const(0x02)
_STATUS_OPTIONS = const(0x03)
_STATUS_TEMP = const(0x04)
_STATUS_SWRST = const(0x7F)

_TIMER_STATUS = const(0x00)
_TIMER_PWM = const(0x01)
_TIMER_FREQ = const(0x02)

_ADC_STATUS = const(0x00)
_ADC_INTEN = const(0x02)
_ADC_INTENCLR = const(0x03)
_ADC_WINMODE = const(0x04)
_ADC_WINTHRESH = const(0x05)
_ADC_CHANNEL_OFFSET = const(0x07)

_SERCOM_STATUS = const(0x00)
_SERCOM_INTEN = const(0x02)
_SERCOM_INTENCLR = const(0x03)
_SERCOM_BAUD = const(0x04)
_SERCOM_DATA = const(0x05)

_NEOPIXEL_STATUS = const(0x00)
_NEOPIXEL_PIN = const(0x01)
_NEOPIXEL_SPEED = const(0x02)
_NEOPIXEL_BUF_LENGTH = const(0x03)
_NEOPIXEL_BUF = const(0x04)
_NEOPIXEL_SHOW = const(0x05)

_TOUCH_CHANNEL_OFFSET = const(0x10)

_HW_ID_CODE = const(0x55)
_EEPROM_I2C_ADDR = const(0x3F)

#TODO: update when we get real PID
_CRICKIT_PID = const(9999)
_ROBOHATMM1_PID = const(9998)



## SEESAW REGISTER MAP
seesawRegs = [0] * 16 # base registers



# Neopixel Register
register_neopixel = [0] * 6

# template registers
regs = [0] * 16
index = 0

# Data to send back on next i2cget command. 
# TODO: implement a proper register map
data = [0] * 16

led = pulseio.PWMOut(board.SERVO1, frequency=5000, duty_cycle=0)

with I2CSlave(board.SCL, board.SDA, [0x49]) as slave:
    while True:
        r = slave.request()
        if not r:
            # Maybe do some housekeeping
            # TODO:  Working functions in here for keeping things going like NeoPixels, etc
            
            continue
        with r:  # Closes the transfer if necessary by sending a NACK or feeding the master dummy bytes
            if DEBUG: print("BEGIN request")
            
            if r.address == 0x49:
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
                        
                        # 0x04 - GPIO (R/W)
                        if moduleFunc == _GPIO_BULK:
                            #n = r.write(bytes([regs[index]]))
                            data = byte(4)

                            if len(data) < 5:
                                print("error: not enough values")
                                continue
                            
                            counter = 0

                            for pin in pins:
                                    data[counter] = pin.value
                                    counter += 1

                            #self.read(_GPIO_BASE, _GPIO_BULK, data)

                        elif moduleFunc == _GPIO_BULK_SET:
                            pass

                    # 0x0E - NeoPixel
                    elif moduleBase == _NEOPIXEL_BASE:
                        # 0x01 - Pin
                        if moduleFunc == _NEOPIXEL_PIN:
                            b = r.read(1)
                            if len(b) < 1:
                                if DEBUG: print("no pin provided")
                                continue
                            register_neopixel[moduleFunc] = b[0]

                        # 0x02 - Speed
                        elif moduleFunc == _NEOPIXEL_SPEED:
                            b = r.read(1)
                            if len(b) < 1:
                                if DEBUG: print("no speed provided")
                                continue
                            register_neopixel[moduleFunc] = b[0]

                        # 0x03 - Buffer Length
                        elif moduleFunc == _NEOPIXEL_BUF_LENGTH:
                            b = r.read(2)
                            if len(b) < 2:
                                if DEBUG: print("no length provided")
                                continue
                            register_neopixel[moduleFunc] = b[0:1]

                        # 0x04 - Data Buffer
                        elif moduleFunc == _NEOPIXEL_BUF:
                            b = r.read(32)
                            if len(b) < 2:
                                if DEBUG: print("packet not long enough")
                                continue
                            register_neopixel[moduleFunc] = b

                        # 0x05 - Show
                        elif moduleFunc == _NEOPIXEL_SHOW:
                            b = r.read(1)
                            if len(b) < 2:
                                if DEBUG: print("not set")
                                continue
                            register_neopixel[moduleFunc] = b[0]
                            if b[0] == 0x01:
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
