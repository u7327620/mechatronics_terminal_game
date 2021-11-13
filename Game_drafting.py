import pyfirmata
from pyfirmata import util
import multiprocessing as mp
from multiprocessing import Pipe
import time
import curses
import os

oxygen_levels = 100.0
voltage_bus_a = 20
voltage_bus_b = 20

#Nature = pyfirmata.Arduino('/dev/ttyUSB1')
#Nature.digital[2].mode = pyfirmata.OUTPUT
#Nature.digital[3].mode = pyfirmata.INPUT

os.environ["TERM"] = "linux"


def Astronautprocess(conn):
    Astronaut = pyfirmata.Arduino('/dev/ttyUSB0')
    Astronaut.digital[2].mode = pyfirmata.OUTPUT
    Astronaut.digital[3].mode = pyfirmata.INPUT
    it = util.Iterator(Astronaut)
    it.start()

    while True:
        pass




#Curses functions
def end_screen(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

def print_text(screen, text):
    screen.clear()
    screen.addstr(0, 0, str(text))
    screen.refresh()

def add_text(screen, dest1, dest2, text):
    screen.addstr(dest1, dest2, str(text))
    screen.refresh()

def flash_home(screen):
    screen.clear()
    print_text(screen, "Welcome to the game\n"
                           "press q to start\n"
                           "press z to exit\n"
                           "press w to count to 100\n"
                           "press e for single blink\n")
    screen.refresh()

def counting():
    i = 0
    while i <100:
        i += 1
        time.sleep(0.01)
        print_text(mainScreen, f'We are at {i}')
    time.sleep(.5)
    flash_home(mainScreen)

def game(astronaut_conn):
    mainScreen.clear()
    while True:
        add_text(mainScreen, 3, 0, f'{astronaut_conn.recv()}')
        add_text(mainScreen, 0, 0, f'Oxygen levels: {oxygen_levels}%')
        add_text(mainScreen, 1, 0, f'Voltage_bus_a: {voltage_bus_a}V')
        add_text(mainScreen, 2, 0, f'Voltage_bus_b: {voltage_bus_b}V')




def screen():
    flash_home(mainScreen)

    while True:
        inp = mainScreen.getch()

        if inp == ord('q'):
            print_text(mainScreen, "Welcome to the game astronaut\n")
            time.sleep(1)
            game()

        if inp == ord('z'):
            end_screen(mainScreen)
            print("Window ended.")
            break

        if inp == ord('w'):
            mainScreen.clear()
            counting()

if __name__ == "__main__":
    game_conn, astronaut_conn = Pipe()
    Astronaut = mp.Process(target=Astronautprocess)
    Astronaut.start()



