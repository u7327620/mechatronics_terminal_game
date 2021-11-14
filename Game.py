import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os
import time

os.environ["TERM"] = "linux"


def dodge(screen, conn, timetoreact, delay, direction):
    if delay is int:
        printtimeandsleep(screen, delay)
    else:
        time.sleep(delay)
    add_text(screen, 0, 0, time.asctime(time.localtime()))
    clear_buffer(conn)
    t_end = time.time() + timetoreact
    add_text(screen, 7, 15, direction)
    clearline(screen, 5)
    while time.time() < t_end:
        if conn.poll() is True:
            msg = conn.recv()
            add_text(screen, 10, 0, msg)
            if direction == "<-- LEFT":
                if msg[0] == 1:
                    clearline(screen, 7)
                    add_text(screen, 7, 0, "| Quickly go:              |")
                    add_text(screen, 5, 0, "Nice Dodge!")
                    return
                if msg[1] == 1:
                    lose(screen, "You went the wrong way and died, how t r a g i c")

            if direction == "RIGHT -->":
                if msg[1] == 1:
                    clearline(screen, 7)
                    add_text(screen, 7, 0, "| Quickly go:              |")
                    add_text(screen, 5, 0, "Nice Dodge!")
                    return
                if msg[0] == 1:
                    lose(screen, "You went the wrong way and died, how t r a g i c")
    lose(screen, "You took too long and your ship got a smooch from a comet ")


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
                clearline(screen, 6)
                add_text(screen, 6, 0, f"Hello Astronaut, this is ground control here, we are going to have lift off "
                                       f"in: {i}\nI am going need you to manage the oxygen and voltage levels"
                                       f" on your ship\nPay attention for messages from me that will pop up down here"
                                       f" as I will be informing you what your buttons do")
                printtimeandsleep(screen, 1)
            clearline(screen, 6, 7, 8)
            add_text(screen, 6, 0, f"We have lift off!")
            printtimeandsleep(screen, 2)
            add_text(screen, 0, 0, time.asctime(time.localtime()))
            clearline(screen, 6)
            add_text(screen, 6, 0, f"Emergency!\n"
                                   f"A comet shower has been knocked off course and is heading directly towards your "
                                   f"ship\nThis is a  t e r r i b l e  coincidence, I'm going to need you to react to "
                                   f"a series of quicktime events because that's how you dodge meteors in a terminal\n"
                                   f"As we all know, comets wait for you to be ready so make sure you have your fingers"
                                   f" on your right and left buttons and press the left button when you are ready")
            while True:
                add_text(screen, 0, 0, time.asctime(time.localtime()))
                msg = astro_conn.recv()
                if msg[0] == 1:
                    break

            clearline(screen, 6, 7, 8, 9, 10)
            add_text(screen, 6, 0, " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
            add_text(screen, 7, 0, "| Quickly go:              |")
            add_text(screen, 8, 0, " __________________________")
            printtimeandsleep(screen, 2)

            # The code in the function looks dumb at first glance but it's just clearing the buffer that built up during
            # the intro process, probably better to make a separate process that handles the controller
            # inputs and passes it to this process but that would take the rest of the day and I need to do maths study
            dodge(screen, astro_conn, 4, 1, "RIGHT -->")
            dodge(screen, astro_conn, 4, 1, "<-- LEFT")
            dodge(screen, astro_conn, 4, 1, "<-- LEFT")
            add_text(screen, 7, 0, "| They're speeding up!     |")
            printtimeandsleep(screen, 1)
            clearline(screen, 7)
            add_text(screen, 7, 0, "| Quickly go:              |")
            dodge(screen, astro_conn, 2, 0.5, "<-- LEFT")
            dodge(screen, astro_conn, 2, 0.5, "RIGHT -->")
            dodge(screen, astro_conn, 1, 0.5, "RIGHT -->")
            dodge(screen, astro_conn, 1, 0.5, "RIGHT -->")
            dodge(screen, astro_conn, 1, 0.5, "<-- LEFT")
            dodge(screen, astro_conn, 1, 0.2, "<-- LEFT")
            dodge(screen, astro_conn, 1, 0.5, "RIGHT -->")
            dodge(screen, astro_conn, 1, 0.2, "RIGHT -->")
            dodge(screen, astro_conn, 1, 0.2, "<-- LEFT")
            dodge(screen, astro_conn, 1, 0.2, "<-- LEFT")
            dodge(screen, astro_conn, 1, 0.2, "RIGHT -->")
            clearline(screen, 4, 5, 6, 7, 8, 9, 10)
            gamereadout(screen, oxy, volta, voltb)
            add_text(screen, 5, 0, "You made it through! Good job astronaut, hopefully no other \n"
                                   "t r a g i c and u n e x p e c t e d coincidences occur during our "
                                   "flight")
            printtimeandsleep(screen, 8)
            clearline(screen, 5, 6)
            add_text(screen, 5, 0, "If you look out your metaphorical window, you'll see the bright spherical "
                                   "mass known as the moon\nAs you should have figured out from your thousands of hours"
                                   " of training, that will be our destination")
            printtimeandsleep(screen, 8)
            for i in range(5):
                printtimeandsleep(screen, 1)
                oxy -= 7.5
                gamereadout(screen, oxy, volta, voltb)
            add_text(screen, 5, 0, "CRITICAL ALERT\nThe oxygen levels are rapidly dropping. We believe the comet shower"
                                   " entered the oxygen tanks personal space and now it's leaking\nWe've sent out the "
                                   "nano bots to fix but we will need you to patch it up temporarily\n"
                                   "Mash the left button to patch!")
            while True:
                msg = astro_conn.recv()
                if msg[0] == 1:
                    break

            t = int(time.time())
            t_end = t + 20
            t1 = t+3
            t2 = t+6
            t3 = t+9
            t4 = t+12
            t5 = t+15
            t6 = t+18
            t_leak = [t1, t2, t3, t4, t5, t6]
            clear_buffer(astro_conn)
            while int(time.time()) < t_end:
                clear_buffer(astro_conn)
                print_time(screen)
                gamereadout(screen, oxy, volta, voltb)
                msg = astro_conn.recv()
                if int(time.time()) in t_leak:
                    oxy -= 15
                    t = int(time.time())
                    t_leak.remove(t)
                if msg[0] == 1:
                    while True:
                        if int(time.time()) in t_leak:
                            oxy -= 7.5
                            t = int(time.time())
                            t_leak.remove(t)
                        msg = astro_conn.recv()
                        if msg[0] == 0:
                            if oxy < 100.0:
                                oxy += 1.0
                            break
                if oxy < 0.0:
                    lose(screen, "You got no more oxygen, you die")

            clearline(screen, 5, 6, 7, 8, 9, 10)
            add_text(screen, 5, 0, "Good job astronaut!, the nano bots have reached the oxygen tank and you\n"
                                   "should now see it filling up ")
            while oxy < 100.0:
                oxy += 1
                gamereadout(screen, oxy, volta, voltb)
                time.sleep(0.01)



if __name__ == "__main__":
    astronaut_conn, game_conn1 = Pipe(True)  # Like mario, we have a pipe to jump message through
    # astronaut_conn2, game_conn2 = Pipe() this one is for luigi! yeah this is deprecated but I like the comment
    # so I'm not removing it
    mainScreen = start_screen()  # Start our screen
    x = mp.Process(target=astro_init, args=('/dev/ttyUSB0', game_conn1,))  # Multiprocess create astro controller
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))  # Multiprocess create the game
    x.start()  # Multiprocess start astro controller process
    y.start()  # Multiprocess start game process
