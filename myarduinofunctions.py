import pyfirmata
from pyfirmata import util
import time


# The code in the clear_buffer looks dumb at first glance
# probably better to make a separate process that handles the controller inputs and passes it to the game process but
# that would take the rest of the day and I need to do maths study

def clear_buffer(conn):
    while True:
        while conn.poll() is True:
            x = conn.recv()
        break

def astro_init(path, conn):  # makes and initialised the board
    Astronaut = pyfirmata.Arduino(path)
    Astronaut.digital[3].mode = pyfirmata.INPUT
    Astronaut.digital[4].mode = pyfirmata.INPUT
    Astronaut.digital[2].mode = pyfirmata.OUTPUT  # the deprecated LED
    it = util.Iterator(Astronaut)  # just for the .read() to work
    it.start()

    conn.send('Init complete')  # The init is important because the board takes like 6 seconds to start the serial
    # connection with pyfirmata
    while True:
        msg = conn.recv()
        if msg == 'blink':  # Gonna leave it in just in case I can come in on monday and plug in an LED
            Astronaut.digital[2].write(1)
            time.sleep(.5)
            Astronaut.digital[2].write(0)
            time.sleep(.5)

        if msg == "button":  # button test
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
                conn.send(msg)  # just a simple joined string

        if msg == 'game':  # when we are gaming
            while True:
                msgtosend = [0, 0]
                if Astronaut.digital[3].read() is True:
                    msgtosend[0] = 1
                if Astronaut.digital[4].read() is True:
                    msgtosend[1] = 1
                conn.send(msgtosend)  # we just constantly send the values of the buttons, yes this fills the buffer
                # Yes it's not the right way to go about it. running a separate process to receive the button output
                # constantly is a much better method. But I don't have the time to do another method
                time.sleep(0.1)  # rockabye baby in the treetops

