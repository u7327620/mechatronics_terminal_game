import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os
import time

os.environ["TERM"] = "linux"

def game(astro_conn, nature_conn, screen):

    flash_home(screen)
    while True:
        inp = screen.getch()

        if inp == ord('w'):
            counting(screen)

        if inp == ord('e'):
            astro_conn.send("blink")
            print_text(screen, f"Should now blink, if not this should be fixed before playing\n"
                               f"wait 5 seconds to return")
            end_time = time.time() + 5
            while True:
                add_text(screen, 3, 0, f'{time.asctime(time.localtime())}')
                msg = astro_conn.recv()
                if msg:
                    add_text(screen, 4, 0, f'The nano has responded with: {msg}')
                if time.time() > end_time:
                    break
            flash_home(screen)



        if inp == ord('q'):
            screen.clear()
            while True:
                msg = astro_conn.recv()
                if msg:
                    print_text(screen, msg)





if __name__ == "__main__":
    astronaut_conn, game_conn = Pipe()
    mainScreen = start_screen()
    x = mp.Process(target=astro_init, args=('/dev/ttyUSB0', game_conn))
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))
    x.start()
    y.start()
