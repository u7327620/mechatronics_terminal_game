import pyfirmata
from pyfirmata import util
import time

def astro_init(path, conn):
    Astronaut = pyfirmata.Arduino(path)
    Astronaut.digital[3].mode = pyfirmata.INPUT
    Astronaut.digital[2].mode = pyfirmata.OUTPUT
    it = util.Iterator(Astronaut)
    it.start()

    while True:
        # x = Astronaut.digital[3].read()
        msg = conn.recv()
        if msg == 'blink':
            conn.send("blinking")
            Astronaut.digital[2].write(1)
            time.sleep(.5)
            Astronaut.digital[2].write(0)
            time.sleep(.5)

        # if x is True:
        #     conn.send("Digital[3] pressed")
        # else:
        #     conn.send("Digital[3] not pressed")

