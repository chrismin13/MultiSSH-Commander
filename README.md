# MultiSSH-Commander
A python3 tool to connect and run a command to multiple SSH servers simultaneously!

# Requirements
This tool uses Paramiko to connect to the SSH Servers! So, make sure to run `pip install paramiko` before using it.

# How to run
After you installed Paramiko, just download `commander.py` from this repo and launch it like any python script: `python3 commander.py`

# Saving and loading
If you click the Save File Button, the program will generate an `entries.json` file with all of the servers, usernames, passwords and commands. **BE CAREFUL!!! The passwords are saved in plain text!!!** So, be careful if you decide to save the options.
The program automatically loads the `entries.json` file when starting up.

## Some general info
This project uses Tkinter for its GUI, and since it's quite small I've scaled it up quite a bit. I'm not particularly worried about security with this, as it's mostly a personal project and not something I'll be deploying more broadly. So, I haven't bothered with SSH RSA Keys or any of the more advanced features that SSH offers. However, if you do want to add them, it shouldn't be that dificult, as Paramiko is quite flexible. I've also got a couple of global variables at the top, if you want to change stuff like the window size and file name for saving.
