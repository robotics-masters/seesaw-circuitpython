## CircuitPython
##  An implementation of SeeSaw in CircuitPython
##
##
import board
import pulseio
import time
import digitalio
from i2cslave import I2CSlave

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

regs = [0] * 16
index = 0

led = pulseio.PWMOut(board.D13, frequency=5000, duty_cycle=0)

with I2CSlave(board.SCL, board.SDA, (0x49)) as slave:
    while True:
        r = slave.request()
        if not r:
            # Maybe do some housekeeping
            continue
        with r:  # Closes the transfer if necessary by sending a NACK or feeding the master dummy bytes
            if r.address == 0x49:
                if not r.is_read:  # Master write which is Slave read
                    first_byte = r.read(1)
                    if first_byte == _STATUS_BASE: ## example register
                        ## code goes here
                        second_byte = r.read(1)

                        if second_byte == _STATUS_HW_ID: ## example pin
                            #  more code required
                            #  look at the old version of this code to see what regs and index is
                            n = r.write(bytes([regs[index]]))

                            chip_id = self.read8(_STATUS_BASE, _STATUS_HW_ID)
                            if chip_id != _HW_ID_CODE:
            					raise RuntimeError("Seesaw hardware ID returned (0x{:x}) is not correct! Expected 0x{:x}. Please check your wiring.".format(chip_id, _HW_ID_CODE))

            		elif first_byte = _EEPROM_BASE
                        ## code goes here
                        second_byte = r.read(1)

                        if second_byte == _EEPROM_I2C_ADDR: ## example pin
                            #  more code required
                            #  look at the old version of this code to see what regs and index is
                            n = r.write(bytes([regs[index]]))


                            i2c_addr = self.read8(_EEPROM_BASE, _EEPROM_I2C_ADDR)

                    elif first_byte == _ADC_BASE
                        second_byte = r.read(1)
                        if second_byte == _ADC_CHANNEL_OFFSET + self.pin_mapping.analog_pins.index(pin)
                            n = r.write(bytes([regs[index]]))
                            third_byte = r.read(1)
                            self.read(_ADC_BASE, _ADC_CHANNEL_OFFSET + self.pin_mapping.analog_pins.index(pin), third_byte)

                    elif first_byte == _GPIO_BASE
                        second_byte = r.read(1)
                        if second_byte == _GPIO_BULK
                            n = r.write(bytes([regs[index]]))
                            data = byte(32)
                            counter = 0

                            for pin in pins:
                                    data[counter] = pin.value
                                    counter += 1

                            self.read(_GPIO_BASE, _GPIO_BULK, data)

                        elif second_byte = _GPIO_BULK_SET
                            n = r.write(bytes([regs[index]]))
                            






                

            ## repeat this for all 8 registers, in each register check how many pins
            ## check what actions each register does 
                ## if register == 0x08
                    ## if pin == servo1
                        ## something with the value
                        ## action

                    
                elif r.is_restart:  # Combined transfer: This is the Master read message
                    n = r.write(bytes([regs[index]]))
                #else:
                    # A read transfer is not supported in this example
                    # If the Master tries, it will get 0xff byte(s) by the ctx manager (r.close())
