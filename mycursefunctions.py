import curses
import time


# Curses functions


def print_time(screen):
    add_text(screen, 0, 0, time.asctime(time.localtime()))

def printtimeandsleep(screen, sleeptime):
    for i in range(sleeptime):
        time.sleep(1)
        print_time(screen)

def gamereadout(screen, oxy, volta, voltb):
    clearline(screen, 3)
    add_text(screen, 0, 100, f'Ship readout')
    add_text(screen, 1, 90, f'=================================')
    add_text(screen, 2, 95, f'Oxygen levels: {oxy}%')
    add_text(screen, 3, 95, f'Voltage bus A: {volta}')
    add_text(screen, 4, 95, f'Voltage bus B: {voltb}')

def lose(screen, msg):
    oxy = 0
    volta = 0
    voltb = 0
    gamereadout(screen, oxy, volta, voltb)
    clearline(screen, 7)
    add_text(screen, 7, 0, msg)
    add_text(screen, 10, 0, "Just like in real life, when you die you have to start over to play again"
                            "\nJust re-run the script to start again")
    end_screen(screen)

def end_screen(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    quit()

def start_screen():
    screen = curses.initscr()  # Initialize screen
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    curses.curs_set(0)
    return screen

def start_window():
    curses.initscr()
    window = curses.newwin(5, 5, 5, 5)
    return window


def print_text(screen, text):
    screen.clear()
    screen.addstr(0, 0, str(text))
    screen.refresh()


def add_text(screen, dest1, dest2, text, *extra):
    if extra:
        screen.addstr(dest1, dest2, str(text), extra[0])
    else:
        screen.addstr(dest1, dest2, str(text))
    screen.refresh()


def flash_home(screen):
    screen.clear()
    print_text(screen, "Welcome to the game\n"
                       "press q for button test\n"
                       "press w for terminal counting test\n"
                       "press e for astronaut blink test\n"
                       "press f to start the game\n")
    screen.refresh()

def counting(screen):
    i = 0
    while i < 100:
        i += 1
        time.sleep(0.01)
        print_text(screen, f'We are at {i}')
    time.sleep(.5)
    flash_home(screen)

def clearline(screen, *lines):
    for line in lines:
        screen.move(line, 0)
        screen.clrtoeol()
