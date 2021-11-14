import curses
import time


# Curses functions


def print_time(screen):  # Deadass a function for a single line of code, made coding easier so I'm not ashamed
    add_text(screen, 0, 0, time.asctime(time.localtime()))

def printtimeandsleep(screen, sleeptime):  # Really just prints the time and sleeps
    for i in range(sleeptime):
        time.sleep(1)
        print_time(screen)

def gamereadout(screen, oxy, volta, voltb):  # Just outputs the ship readout
    clearline(screen, 2, 3, 4)
    add_text(screen, 0, 100, f'Ship readout')
    add_text(screen, 1, 90, f'=================================')
    add_text(screen, 2, 95, f'Oxygen levels: {oxy}%')
    add_text(screen, 3, 95, f'Voltage bus A: {volta}')
    add_text(screen, 4, 95, f'Voltage bus B: {voltb}')

def lose(screen, msg):  # When you lose
    oxy = 0
    volta = 0
    voltb = 0
    gamereadout(screen, oxy, volta, voltb)
    clearline(screen, 7)
    add_text(screen, 7, 0, msg)
    add_text(screen, 10, 0, "Just like in real life, when you die you have to start over to play again"
                            "\nJust re-run the script to start again")
    end_screen(screen)  # Just ends the terminal and script

def end_screen(screen):  # Function to end the terminal
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    quit()  # Built-in python method to end a script

def start_screen():  # Screen init
    screen = curses.initscr()  # Initialize screen
    curses.noecho()  # Doesn't echo the characters pressed back
    curses.cbreak()  # Doesn't accept keyboard interrupts
    screen.keypad(True)  # Stops exit schemes like ctrl + c from exiting
    curses.curs_set(0)  # Invisible cursor!
    return screen  # Return the screen we make

def start_window():  # Not going to get rid of it as it's still useful but isn't used currently
    curses.initscr()
    window = curses.newwin(5, 5, 5, 5)
    return window


def print_text(screen, text):  # pretty self explanatory
    screen.clear()
    screen.addstr(0, 0, str(text))
    screen.refresh()


def add_text(screen, dest1, dest2, text, *extra):  # Allows for A_DIM to be passed and is a general text func without
    # screen.clear()
    if extra:
        screen.addstr(dest1, dest2, str(text), extra[0])
    else:
        screen.addstr(dest1, dest2, str(text))
    screen.refresh()


def flash_home(screen):  # Just flashes the main menu screen
    screen.clear()
    print_text(screen, "Welcome to the game\n"
                       "press q for button test\n"
                       "press w for terminal counting test\n"
                       "press e for astronaut blink test\n"
                       "press f to start the game\n")
    screen.refresh()

def counting(screen):  # terminal counting test
    i = 0
    while i < 100:
        i += 1
        time.sleep(0.01)
        print_text(screen, f'We are at {i}')
    time.sleep(.5)
    flash_home(screen)

def clearline(screen, *lines):  # Ah yes, the holy line clearing function. Fun fact: I only made this recursive
    # after using the function for the 50th time in like 10 minutes
    for line in lines:
        screen.move(line, 0)
        screen.clrtoeol()
