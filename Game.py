import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os
import time

os.environ["TERM"] = "linux"

def game(astro_conn, nature_conn, screen):  # main process, takes inputs from the controllers

    print_text(screen, "Initializing...")  # Just waiting until the nano sends a message back
    while True:
        if astro_conn.recv() == "Init complete":
            break

    flash_home(screen)  # Ye olde "gimme a menu screen" call, every good program has to have this

    while True:  # First while True, menu screen / test screen
        inp = screen.getch()  # This is the little dude handling our keyboard inputs

        if inp == ord('w'):  # If a w then do the counting test
            counting(screen)

        if inp == ord('e'):  # if an e then do the blink test
            astro_conn.send("blink")  # communicating that we wanna blink, communication is very important yknow
            print_text(screen, f"Should now blink, if not this should be fixed before playing\n"
                               f"wait 5 seconds to return")  # A juicy message to our players
            end_time = time.time() + 5  # creating a variable that is 5 seconds into the future!!!!
            while True:
                add_text(screen, 3, 0, f'{time.asctime(time.localtime())}')  # just updating our time passed
                if time.time() > end_time:
                    break
            flash_home(screen)  # Oh how I love our "gimme a menu screen" call

        if inp == ord('q'):  # if a q, do button test
            astro_conn.send("button")  # communicating that we want to button test, very important
            end_time = time.time() + 4  # 4 seconds into the future!
            while time.time() < end_time:
                msg = astro_conn.recv()  # If you only tell things what to do and never listen, you will never truly
                print_text(screen, msg)  # get a strong understanding of what is going on
            flash_home(screen)  # My dearest menu screen, oh please cometh back and bless thine eyes with your presence

        if inp == ord('f'):  # if F, game time boys
            astro_conn.send('game')  # I deadass told the controllers "game" I think it's kinda funny tbh
            gametime(screen, 100.0, 5, 5)



if __name__ == "__main__":
    astronaut_conn, game_conn = Pipe()  # Like mario, we have a pipe to jump message through
    mainScreen = start_screen()  # Start our screen
    x = mp.Process(target=astro_init, args=('/dev/ttyUSB0', game_conn))  # Multiprocess create astro controller
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))  # Multiprocess create the game
    x.start()  # Multiprocess start astro controller process
    y.start()  # Multiprocess start game process