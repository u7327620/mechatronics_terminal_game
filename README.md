# mechatronics_terminal_game

This is for my year 11 mechatronics class. Really just using the repo to look through and visualise the design process over time. 
Should you wish to re-create the project ...

The code requires an arduino with a button input on port 3 and 4. The arduino needs to be runningstandard firmata from the arduino
ide sketch library. Make sure to update the path variable to that of your arduino.

This was all made in pycharm venv with terminal emulation, if you want to run it without a venv you can make your own exe
because I got maths to study for 😎

The game should work cross platform as long as the os.environ variable is changed to the operating system of choice

Step by Step:

1: git clone {this repo}
2: navigate to the repo on your file system
3: python3 -m venv {Path to this repo}
4: navigate to the bin folder
5: source activate  # You have now made the python virtual environment
6: exit the bin folder and enter the game folder
7: pip3 install -r requirements.txt
8: Change the os.environm["TERM"] = To your operating system
9: Change the path = to the arduino controller usb port
10: python3 Game.py
