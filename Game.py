import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os

os.environ["TERM"] = "linux"

def game(astro_conn, nature_conn, screen):

    while True:
        msg = astro_conn.recv()
        add_text(screen, 0, 0, msg)


if __name__ == "__main__":
    astronaut_conn, game_conn = Pipe()
    mainScreen = start_screen()
    x = mp.Process(target=astro_init, args=('/dev/ttyUSB0', game_conn))
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))
    x.start()
    y.start()
