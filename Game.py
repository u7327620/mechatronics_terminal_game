import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os
import time

os.environ["TERM"] = "linux"


def game(astro_conn, nature_conn, screen):  # main process, takes inputs from the controllers
    print_text(screen, "Initializing...")  # Just waiting until the two nanos sends a message back
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
            end_time = time.time() + 6  # 4 seconds into the future!
            while time.time() < end_time:
                if astro_conn.poll() is True:
                    msg = astro_conn.recv()  # If you only tell things what to do and never listen, you will never truly
                    print_text(screen, msg)  # get a strong understanding of what is going on
            flash_home(screen)  # My dearest menu screen, oh please cometh back and bless thine eyes with your presence

        if inp == ord('f'):  # if F, game time boys
            astro_conn.send('game')  # une bruh momento game funi innit buv こわいおね？

            oxy = 100.0
            volta = 5
            voltb = 5
            screen.clear()

            gamereadout(screen, oxy, volta, voltb)
            for i in range(10, -1, -1):
                add_text(screen, 0, 0, time.asctime(time.localtime()))
                clearline(screen, 6)
                add_text(screen, 6, 0, f"Hello Astronaut, this is ground control here, we are going to have lift off "
                                       f"in: {i}\nI am going need you to manage the oxygen and voltage levels"
                                       f" on your ship\nPay attention for messages from me that will pop up down here"
                                       f" as I will be informing you what your buttons do")
                time.sleep(1)
            clearline(screen, 6)
            clearline(screen, 7)
            clearline(screen, 8)
            add_text(screen, 6, 0, f"We have lift off!")
            time.sleep(2)
            add_text(screen, 0, 0, time.asctime(time.localtime()))
            clearline(screen, 6)
            add_text(screen, 6, 0, f"Emergency!\n" 
                                   f"A comet shower has been knocked off course and is heading directly towards your "
                                   f"ship\nThis is a  t e r r i b l e  coincidence, I'm going to need you to react to "
                                   f"a series of quicktime events because that's how you dodge meteors in a terminal\n"
                                   f"Make sure you have your fingers on your right and left buttons and press the left "
                                   f"button when you are ready")
            while True:
                add_text(screen, 0, 0, time.asctime(time.localtime()))
                astro_conn.send('req')
                msg = astro_conn.recv()
                if msg[0] == 1:
                    break
            clearline(screen, 6)
            clearline(screen, 7)
            clearline(screen, 8)
            clearline(screen, 9)
            add_text(screen, 6, 0, " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
            add_text(screen, 7, 0, "| Quickly go:              |")
            add_text(screen, 8, 0, " __________________________")
            time.sleep(2)
            t_end = time.time() + 4
            add_text(screen, 7, 15, "RIGHT -->")
            astro_conn.send("req")
            while time.time() < t_end:
                if astro_conn.poll() is True:
                    msg = astro_conn.recv()
                    if msg[1] == 1:
                        clearline(screen, 7)
                        add_text(screen, 7, 0, "| Quickly go:              |")
                        add_text(screen, 5, 0, "Nice Dodge!")
                    if msg[0] == 1:
                        oxy = 0
                        volta = 0
                        voltb = 0
                        gamereadout(screen, oxy, volta, voltb)
                        clearline(screen, 7)
                        add_text(screen, 7, 0, "You went the wrong way and died, how t r a g i c")







if __name__ == "__main__":
    astronaut_conn, game_conn1 = Pipe(True)  # Like mario, we have a pipe to jump message through
    # astronaut_conn2, game_conn2 = Pipe() this one is for luigi! yeah this is deprecated but I like the comment
    # so I'm not removing it
    mainScreen = start_screen()  # Start our screen
    x = mp.Process(target=astro_init, args=('/dev/ttyUSB0', game_conn1,))  # Multiprocess create astro controller
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))  # Multiprocess create the game
    x.start()  # Multiprocess start astro controller process
    y.start()  # Multiprocess start game process
