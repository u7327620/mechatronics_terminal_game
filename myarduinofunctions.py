import pyfirmata
from pyfirmata import util
import time

def astro_init(path, conn):
    Astronaut = pyfirmata.Arduino(path)
    Astronaut.digital[3].mode = pyfirmata.INPUT
    it = util.Iterator(Astronaut)
    it.start()

    while True:
        x = Astronaut.digital[3].read()
        if x is True:
            conn.send("Digital[3] pressed")
        else:
            conn.send("Digital[3] not pressed")
        time.sleep(.05)
