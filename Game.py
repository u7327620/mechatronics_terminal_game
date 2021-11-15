import multiprocessing as mp
from multiprocessing import Pipe
from mycursefunctions import *
from myarduinofunctions import *
import os
import time

os.environ["TERM"] = "linux"  # sets environment for curses
path = '/dev/ttyUSB0'


def dodge(screen, conn, timetoreact, delay, direction):  # This is the dodge function for the first quicktime event
    # it's here because it didn't really fit into any other file and I didn't want to make a game functions file
    if delay is int:  # Probably a better way but oh well, tries to use printtimeandsleep() wherever possible
        printtimeandsleep(screen, delay)
    else:
        time.sleep(delay)  # uses time.sleep as backup
    add_text(screen, 0, 0, time.asctime(time.localtime()))  # Bruh I really made this print anyway
    clear_buffer(conn)
    t_end = time.time() + timetoreact  # When to end the event
    add_text(screen, 7, 15, direction)
    clearline(screen, 5)
    while time.time() < t_end:  # While we haven't ended
        if conn.poll() is True:  # poll() just checks if there's anything to receive, this is just here for efficiency
            msg = conn.recv()
            add_text(screen, 10, 0, msg)  # Outputs the little [0, 0] at the bottom of the screen
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


def game(astro_conn, nature_conn, screen):  # Runs the menu screen and game
    print_text(screen, "Initializing...")  # Just waiting until the nano sends a message back
    while True:
        if astro_conn.recv() == "Init complete":
            break

    flash_home(screen)  # Ye olde "gimme a menu screen" call, every good program has to have this

    while True:  # First while True, menu screen / test screen
        inp = screen.getch()  # This is the little dude handling our keyboard inputs

        if inp == ord('w'):  # If a w then do the counting test
            counting(screen)

        if inp == ord('e'):  # if an e then do the blink test, this is deprecated solely because I didn't have enough
            # resistors to put leds on the board
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
                if astro_conn.poll() is True:  # If we get a message:
                    msg = astro_conn.recv()  # If you only tell things what to do and never listen, you will never truly
                    print_text(screen, msg)  # get a strong understanding of what is going on
            flash_home(screen)  # My dearest menu screen, oh please cometh back and bless thine eyes with your presence

        if inp == ord('f'):  # if F, game time boys
            astro_conn.send('game')  # tell the controller we are gaming

            oxy = 100.0
            volta = 20
            voltb = 20
            screen.clear()

            gamereadout(screen, oxy, volta, voltb)  # gamereadout() just does the ship readout you see on screen
            for i in range(10, -1, -1):
                clearline(screen, 6)  # My very beautiful recursive line clearer
                add_text(screen, 6, 0, f"Hello Astronaut, this is ground control here, we are going to have lift off "
                                       f"in: {i}\nI am going need you to manage the oxygen and voltage levels"
                                       f" on your ship\nPay attention for messages from me that will pop up down here"
                                       f" as I will be informing you what your buttons do")
                printtimeandsleep(screen, 1)  # my very beautiful sleeper that also prints time
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
            clear_buffer(astro_conn)  # my very beautiful buffer clearer, just uses recv() until there is nothing left
            while True:
                add_text(screen, 0, 0, time.asctime(time.localtime()))
                msg = astro_conn.recv()
                if msg[0] == 1:
                    break

            clearline(screen, 6, 7, 8, 9, 10)
            add_text(screen, 6, 0, " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")  # The box looks cool right?
            add_text(screen, 7, 0, "| Quickly go:              |")
            add_text(screen, 8, 0, " __________________________")
            printtimeandsleep(screen, 2)
            dodge(screen, astro_conn, 4, 1, "RIGHT -->")  # Just does the quicktime event, look at the top of this file
            # for deets
            dodge(screen, astro_conn, 4, 1, "<-- LEFT")
            dodge(screen, astro_conn, 4, 1, "<-- LEFT")
            add_text(screen, 7, 0, "| They're speeding up!     |")
            printtimeandsleep(screen, 1)
            clear_buffer(astro_conn)  # Clear buffer after the sleep to maximize efficiency
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
                                   "flight")  # hahahahaha I'm so f u n n y
            printtimeandsleep(screen, 8)
            clearline(screen, 5, 6)
            add_text(screen, 5, 0, "If you look out your metaphorical window, you'll see the bright spherical "
                                   "mass known as the moon\nAs you should have figured out from your thousands of hours"
                                   " of training, that will be our destination")  # Omg another funny? what a comedian
            printtimeandsleep(screen, 8)
            for i in range(5):
                printtimeandsleep(screen, 1)
                oxy -= 7.5
                gamereadout(screen, oxy, volta, voltb)
            add_text(screen, 5, 0, "CRITICAL ALERT\nThe oxygen levels are rapidly dropping. We believe the comet shower"
                                   " entered the oxygen tanks personal space and now it's leaking\nWe've sent out the "
                                   "nano bots to fix but we will need you to patch it up temporarily\n"
                                   "Mash the left button to patch!")  # Nano bots?!?!?!
            while True:  # Only start dropping after first button press
                msg = astro_conn.recv()
                if msg[0] == 1:
                    break

            t = int(time.time())
            t_end = t + 20
            t1 = t + 3
            t2 = t + 6
            t3 = t + 9
            t4 = t + 12
            t5 = t + 15
            t6 = t + 18
            t_leak = [t1, t2, t3, t4, t5, t6]  # Time stamps to drop the oxy levels
            clear_buffer(astro_conn)
            while int(time.time()) < t_end:
                clear_buffer(astro_conn)  # Yea it works, once again not a good idea to call here but it works so shut!
                print_time(screen)
                gamereadout(screen, oxy, volta, voltb)
                msg = astro_conn.recv()
                if int(time.time()) in t_leak:  # if on a time stamp
                    oxy -= 18  # oof your oxygen
                    t = int(time.time())
                    t_leak.remove(t)  # Remove time stamp

                # This next bit looks weird, but it's just to make sure we count individual button presses by only
                # activating when we have pressed and unpressed the button. If we didn't do this, the player can just
                # hold down the button and win!
                if msg[0] == 1:  # When button pressed
                    while True:
                        if int(time.time()) in t_leak:  # Can't hold down the button and stop taking oxy damage
                            oxy -= 18
                            t = int(time.time())
                            t_leak.remove(t)
                        msg = astro_conn.recv()  # check for updates
                        if msg[0] == 0:  # When unpressed
                            if oxy < 100.0:  # not over 100
                                oxy += 1.0  # Add 1 oxy
                            break
                if oxy <= 0.0:  # If you don't keep oxy up enough
                    clearline(screen, 5, 6, 7, 8, 9, 10)
                    lose(screen, "You got no more oxygen, you die")

            clearline(screen, 5, 6, 7, 8, 9, 10)
            add_text(screen, 5, 0, "Good job astronaut!, the nano bots have reached the oxygen tank and you\n"
                                   "should now see it filling up ")
            while oxy < 100.0:
                oxy += 1
                gamereadout(screen, oxy, volta, voltb)
                time.sleep(0.1)
            oxy = 100.0  # Sometimes goes to 100.5 and I can't be bothered to fix it in the previous loop
            gamereadout(screen, oxy, volta, voltb)
            printtimeandsleep(screen, 1)
            clearline(screen, 5, 6)
            add_text(screen, 5, 0, "Your metaphorical cabin shakes as the ship lowers to the moons surface\n"
                                   "You've done it, you're on the moon surface. As you exit your craft you see a"
                                   " group of 30 aliens")  # Omg Aliens!!!
            printtimeandsleep(screen, 4)
            for i in range(3):  # Got to drop the volt for the last 3 seconds of our 7 second wait
                printtimeandsleep(screen, 1)
                volta -= 1
                voltb -= 1
                gamereadout(screen, oxy, volta, voltb)
            clearline(screen, 5, 6)
            add_text(screen, 5, 0, "Critical Alert\n"
                                   "These aliens are the well known electro succ aliens\n"
                                   "They're stealing our volts! You're going to die! Remove any doubts in your mind"
                                   " it's us or them\n"  # Csgo reference anyone?
                                   "Quickly astronaut, commit genocide on their species by mashing the "
                                   "left button!\n")  # haha funni genocide. Please don't be like the youtube algorithm
            # and mark me down because I said genocide. I mean, we literally are killing all the natives because they
            # are taking our lifeline away. Plus that's like story wise and not mechamatronic wise
            clear_buffer(astro_conn)  # Thine buffeth be looking undoubtedly thicceth, no cappeth
            while True:
                msg = astro_conn.recv()
                if msg[0] == 1:
                    break
            t = int(time.time())
            t1 = t + 2
            t2 = t + 4
            t3 = t + 6
            t4 = t + 8
            t5 = t + 10
            t6 = t + 12
            t7 = t + 14
            t8 = t + 16
            t9 = t + 18
            t10 = t + 20
            t_yoink = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]  # time stamps for volt yoink
            aliens = 30
            clearline(screen, 5, 6, 7, 8, 9)
            clear_buffer(astro_conn)
            while volta > 0 and aliens > 0:  # I'm not going to re-comment this, it's the same as the previous
                # "mash the button" except with aliens and volts
                voltb = volta
                clearline(screen, 5)
                add_text(screen, 5, 0, f"Aliens left: {aliens}")
                gamereadout(screen, oxy, volta, voltb)
                msg = astro_conn.recv()
                if int(time.time()) in t_yoink:
                    volta -= 3
                    t_yoink.remove(int(time.time()))
                if msg[0] == 1:
                    while True:
                        if int(time.time()) in t_yoink:
                            volta -= 3
                            t_yoink.remove(int(time.time()))
                        msg = astro_conn.recv()
                        if msg[0] == 0:
                            aliens -= 1
                            break
            if volta < 0:
                lose(screen, "They zucced your volts away and you died on the moon")  # haha funni zucc

            if aliens <= 0:
                clearline(screen, 5, 6, 7, 8, 9)
                add_text(screen, 5, 0, "Good job astronaut! The natives have been exterminated!\n"
                                       "We have a big PR issue down here on earth so we're going to have to pull you"
                                       " out now\nLet's get you back home in time for chow")  # Csgo reference btw
                printtimeandsleep(screen, 12)

            clearline(screen, 5, 6, 7, 8, 9)
            print_text(screen, "And that's all folks, hope you enjoyed your journey")  # game end
            end_screen(screen)


if __name__ == "__main__":  # This is just a funky python guard that will stop the script from causing issues if
    # accidentally imported instead of directly run. Very unlikely that it will be but, hey, I've done dumber!
    astronaut_conn, game_conn1 = Pipe(True)  # Like mario, we have a pipe to jump messages through
    mainScreen = start_screen()  # Start our screen
    x = mp.Process(target=astro_init, args=(path, game_conn1,))  # Multiprocess create astro controller
    y = mp.Process(target=game, args=(astronaut_conn, 0, mainScreen))  # Multiprocess create the game
    x.start()  # Multiprocess start astro controller process
    y.start()  # Multiprocess start game process
