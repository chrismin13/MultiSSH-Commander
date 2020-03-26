### THIS REQUIRES PARAMIKO!!!!!
### pip install paramiko

##### ===== ENTRY TEXT ===== #####
FILENAME='entries.json'
ENTRY_LENGTH = 8

HEIGHT = 400
WIDTH = 800
SCALING=1.6

##### ===== ========== ===== #####

##### ===== LOAD / SAVE ===== #####

import json

file = open(FILENAME, 'r')
entryText=json.load(file)
file.close()

def loadFile():
    file = open(FILENAME, 'r')
    entryText=json.load(file)
    file.close()


def saveFile():
    file = open(FILENAME, 'w')
    json.dump(entryText, file, indent=4, sort_keys=True)
    file.close()



##### ===== COMMAND RUN ===== #####

import paramiko
import threading

# RUN ALL BUTTON
def runAll():
    for i in range(0,ENTRY_LENGTH):
        closeThread(i)
        runThread(i)

# STOP ALL BUTTON
def stopAll():
    for i in range(0,ENTRY_LENGTH):
        closeThread(i)

## Must be multithreaded, as we want the commands to run at 
## the same time and not freeze up the program in the process.
running = [] # Keeps tracks of what's running so we can cancel it
for i in range(0,ENTRY_LENGTH):
    running.append(None)

def closeThread(i):
    if running[i] != None:
        temp = running[i]
        running[i] = None
        temp.close()
        run = runButton[i]
        run.config(text="Cancelled", bg='tomato')

def runThread(i):
    if running[i] != None:
        closeThread(i)
    else:
        thread = threading.Thread(target = runOne, args=(i,), name = "SSH Connection to " + str(i), daemon=True)
        thread.start()

def runOne(i):   
    address = addressEntry[i]
    user = userEntry[i]
    password = passEntry[i]
    cmd = cmdEntry[i]
    run = runButton[i]
    # Reset button styling before running
    run.config(text='Run', bg='SystemButtonFace')
    if address.get().strip() != '' and user.get().strip() != '' and password.get().strip() != '' and cmd.get().strip() != '':
        try:
            running[i] = paramiko.SSHClient() # Store it, so we can stop it if needed

            run.config(text="Connecting", bg='gold')
            running[i].set_missing_host_key_policy(paramiko.AutoAddPolicy())
            running[i].connect(address.get(), port=22, username=user.get(), password=password.get())
            
            stdin, stdout, stderr = running[i].exec_command(cmd.get(), get_pty=True) # get_pty=True so we can terminate it
            run.config(text="Running", bg='yellow')
            print (stdout.readlines()) # This hangs it until it's done
            
            if running[i] is not None:
                running[i].close()
                run.config(text="Finished", bg='green2')
        except Exception as e:
            if (running[i] != None): # Check if we stopped it
                run.config(text="Error", bg='brown1')
                print(e)

##### ===== =========== ===== #####


##### ===== GUI ===== #####

from tkinter import *

rely=0
relheight=0.09
relgap=0.01

# Remember, there's the relgap in between! They'll add up to 1.
# That means: sizes[0] + relgap + sizes[1] + relgap (...etc) + sizes[last] = 1
sizes = [0.15, 0.11, 0.11, 0.50, 0.09]

# Calculate the space and relative positions as shown above
def relx(order):
    relx = 0
    if order != 1: # No gap in the begining, as the frame already has a gap.
        for i in range(1, order):
            if sizes[i-1] != None:
                relx = relx + sizes[i-1] + relgap
    return relx


root = Tk()
root.tk.call('tk', 'scaling', SCALING) # Makes it a litle more readable

# Canvas
canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Frame
frame = Frame(root)
frame.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

# Labels at the top
addressLabel = Label(frame, text='Address', anchor='w')
addressLabel.place(relx=relx(1), rely=rely, relwidth=sizes[0], relheight=relheight)

addressLabel = Label(frame, text='Username', anchor='w')
addressLabel.place(relx=relx(2), rely=rely, relwidth=sizes[1], relheight=relheight)

addressLabel = Label(frame, text='Password', anchor='w')
addressLabel.place(relx=relx(3), rely=rely, relwidth=sizes[2], relheight=relheight)

addressLabel = Label(frame, text='Command', anchor='w')
addressLabel.place(relx=relx(4), rely=rely, relwidth=sizes[3], relheight=relheight)

rely = rely + relheight # No gap here

# Entries and Buttons
addressEntry = []
userEntry = []
passEntry = []
cmdEntry = []
runButton = []

# When I place the items, I make sure that the relative width and height adds up to 1.
# You can figure that out by adding relx+relwidth or rely+relheight for every one.
for i in range(0,ENTRY_LENGTH):
    addressEntry.append(Entry(frame))
    addressEntry[i].place(relx=relx(1), rely=rely, relwidth=sizes[0], relheight=relheight)
    addressEntry[i].insert(0, entryText[i][0])
   
    userEntry.append(Entry(frame))
    userEntry[i].place(relx=relx(2), rely=rely, relwidth=sizes[1], relheight=relheight)
    userEntry[i].insert(0, entryText[i][1])

    passEntry.append(Entry(frame, show="*"))
    passEntry[i].insert(0, entryText[i][2])
    passEntry[i].place(relx=relx(3), rely=rely, relwidth=sizes[2], relheight=relheight)

    cmdEntry.append(Entry(frame))
    cmdEntry[i].insert(0, entryText[i][3])
    cmdEntry[i].place(relx=relx(4), rely=rely, relwidth=sizes[3], relheight=relheight)

    runButton.append(Button(frame, text="Run", command= lambda now=i: runThread(int(now))))
    runButton[i].place(relx=relx(5), rely=rely, relwidth=sizes[4], relheight=relheight)

    rely = rely + relheight + relgap

# Bottom section
## Run all button
runAll = Button(frame, text="Run All", command=runAll)
runAll.place(relx=0.53, rely=0.9, relwidth=0.1, relheight=0.1)

## Stop all
stopAll = Button(frame, text="Stop All", command=stopAll)
stopAll.place(relx=0.64, rely=0.9, relwidth=0.1, relheight=0.1)

## Load from File
loadFromFile = Button(frame, text="Load File", command=loadFile)
loadFromFile.place(relx=0.37, rely=0.9, relwidth=0.1, relheight=0.1)

## Save to file
saveToFile = Button(frame, text="Save File", command=saveFile)
saveToFile.place(relx=0.26, rely=0.9, relwidth=0.1, relheight=0.1)

# Done with the UI render!
root.mainloop()