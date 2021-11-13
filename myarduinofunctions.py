import pyfirmata
from pyfirmata import util
import time


def astro_init(path, conn):
    Astronaut = pyfirmata.Arduino(path)
    Astronaut.digital[3].mode = pyfirmata.INPUT
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
                    msg = 'pressed'
                else:
                    msg = 'not pressed'
                conn.send(msg)
                time.sleep(.05)

        if msg == 'game':
            while True:
                msg = []
                if Astronaut.digital[3].read() is True:
                    msg.append("b1 p")
                conn.send(msg)

def nature_init(path, conn):
    Nature = pyfirmata.Arduino(path)
    Nature.digital[1].mode = pyfirmata.INPUT
    Nature.digital[2].mode = pyfirmata.OUTPUT
    it = util.Iterator(Nature)
    it.start()

    conn.send('Init complete')
    while True:
        # x = Astronaut.digital[3].read()
        msg = conn.recv()
        if msg == 'blink':
            Nature.digital[2].write(1)
            time.sleep(.5)
            Nature.digital[2].write(0)
            time.sleep(.5)

        if msg == "button":
            end_time = time.time() + 5
            while time.time() < end_time:
                if Nature.digital[3].read() is True:
                    msg = 'pressed'
                else:
                    msg = 'not pressed'
                conn.send(msg)
                time.sleep(.05)

        if msg == 'game':
            while True:
                msg = []
                if Nature.digital[3].read() is True:
                    msg.append("b1 p")
                conn.send(msg)
