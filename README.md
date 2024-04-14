# mechatronics_terminal_game

11th grade mechatronics class project. Uses arduino hardware for interactions. To re-create the controller:

Use an Arduino uno with 2 button inputs, one on port 3 and one on port 4. The arduino needs to run standard firmata from the arduinoide sketch library. **Make sure to update the path variable in the game-code to match the Arduino.**

Only tested on unix system using a terminal supporting curses library. Compatibility issues will lie with the curses library.


Step by Step without Venv:

1: `git clone {this repo}`

2: navigate to the repo on your file system

3: `pip3 install -r requirements.txt`

4: change `os.environm["TERM"] = ` To your terminal

5: change `path = ` to the arduino controller usb port

6: `python3 Game.py`


or


Step by Step with Venv:

1: `git clone {this repo}`

2: navigate to the repo on your file system

3: `python3 -m venv {Path to this repo}`

4: navigate to the bin folder

5: `source activate` 

6: exit the bin folder and enter the game folder

7: `pip3 install -r requirements.txt`

8: Change `os.environm["TERM"] = ` To your terminal

9: Change `path = ` to the arduino controller usb port

10: `python3 Game.py`



