import pyfirmata
from pyfirmata import util
import time


def astro_init(path, conn):
    Astronaut = pyfirmata.Arduino(path)
    Astronaut.digital[3].mode = pyfirmata.INPUT
    Astronaut.digital[4].mode = pyfirmata.INPUT
    Astronaut.digital[2].mode = pyfirmata.OUTPUT
    it = util.Iterator(Astronaut)
    it.start()

    conn.send('Init complete')
    while True:
        # x = Astronaut.digital[3].read()
        msg = conn.recv()
        if msg == 'blink':
            Astronaut.digital[2].write(1)
            time.sleep(.5)
            Astronaut.digital[2].write(0)
            time.sleep(.5)

        if msg == "button":
            end_time = time.time() + 5
            while time.time() < end_time:
                if Astronaut.digital[3].read() is True:
                    msg = 'pressed, '
                else:
                    msg = 'not pressed, '
                if Astronaut.digital[4].read() is True:
                    msg += 'pressed'
                else:
                    msg += 'not pressed'
                conn.send(msg)

        if msg == 'game':
            while True:
                msgtosend = [0, 0]
                if Astronaut.digital[3].read() is True:
                    msgtosend[0] = 1
                if Astronaut.digital[4].read() is True:
                    msgtosend[1] = 1
                conn.send(msgtosend)
