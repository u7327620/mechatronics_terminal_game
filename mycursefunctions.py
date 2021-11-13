import curses
import time


# Curses functions

def gametime(screen, oxy, volta, voltb):
    screen.clear()
    add_text(screen, 0, 10, f'Ship readout')
    add_text(screen, 1, 0, f'=================================')
    add_text(screen, 2, 0, f'Oxygen levels: {oxy}%')
    add_text(screen, 3, 0, f'Voltage bus A: {volta}')
    add_text(screen, 4, 0, f'Voltage bus B: {voltb}')


def end_screen(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()


def start_screen():
    screen = curses.initscr()  # Initialize screen
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return screen


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
