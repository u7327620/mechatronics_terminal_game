import curses


# Curses functions
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
                           "press q to start\n"
                           "press z to exit\n"
                           "press w to count to 100\n"
                           "press e for single blink\n")
    screen.refresh()
