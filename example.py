import board
from i2cslave import I2CSlave

# fake registers (think of these like real ones)
#  this simulation only has 1 register with 16 parts
regs = [0] * 16
# next register to read from after i2cset
index = 0

## DEBUG TOGGLE - output on REPL
DEBUG = True


with I2CSlave(board.SCL, board.SDA, (0x40, 0x42)) as slave:
    while True:
        r = slave.request()
        if not r:
            # Maybe do some housekeeping
            continue
        with r:  # Closes the transfer if necessary by sending a NACK or feeding the master dummy bytes
            if DEBUG: print("BEGIN request")
            
            # choose a I2C Address.  We can simulate as many requests as we like for this.
            if r.address == 0x40:
                if DEBUG: print("ADDRESS 0x40")
                
                # This is used by i2cset commands (or similar) and sets which register is next to be read from.
                #  No write requests can take place in this section.
                if not r.is_read:  # Master write which is Slave read
                    if DEBUG: print("slave read")
                    
                    # Read in first byte - the 'fake' register location.
                    b = r.read(1)
                    if not b or b[0] > 15:
                        if DEBUG: print("empty byte")
                        continue
                        
                    # set the 'fake' register location we want to right to next.
                    index = b[0]
                    
                    # read in second byte of data.  This corresponds to the specific data we want to 
                    #  put into the 'fake' register.
                    b = r.read(1)
                    if b:
                        if DEBUG: print("data: ", b[0])
                        regs[index] = b[0]
                        
                # This is used by i2cget commands (or similar) and reads back the register that is set as 
                #  index.  No read transactions can take place in this section.
                elif r.is_restart:  # Combined transfer: This is the Master read message
                    if DEBUG: print("combined transfer")
                    n = r.write(bytes([regs[index]]))
                #else:
                    # A read transfer is not supported in this example
                    # If the Master tries, it will get 0xff byte(s) by the ctx manager (r.close())
            elif r.address == 0x42:
                if DEBUG: print("ADDRESS 0x42")
                if not r.is_read:
                    b = r.read(1)
                    if b and b[0] == 0xde:
                        # do something
                        pass
