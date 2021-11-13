import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os

os.environ["TERM"] = "linux"

def game(astro_conn, nature_conn, screen):

    flash_home(screen)
    while True:
        inp = screen.getch()

        if inp == ord('w'):
            counting(screen)

        if inp == ord('e'):
            astro_conn.send('blink')
            print_text(screen, f"Should now blink\n"
                               f"press any key to retun\n")
            while True:
                retur = screen.getch()
                if retur:
                    flash_home(screen)
                    break

        if inp == ord('q'):
            while True:
                msg = astro_conn.recv()
                print_text(screen, msg)





if __name__ == "__main__":
    astronaut_conn, game_conn = Pipe()
    mainScreen = start_screen()
    x = mp.Process(target=astro_init, args=('/dev/ttyUSB0', game_conn))
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))
    x.start()
    y.start()
