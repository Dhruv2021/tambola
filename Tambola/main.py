import socket
from tkinter import *
from threading import Thread
import random
from PIL import ImageTk, Image
from tkinter import Button, Label, Frame
import random
import platform


screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None

nameEntry = None
nameWindow = None


def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())


def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry('800x600')

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./background.png")

    canvas1 = Canvas(nameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True)
    # Display image
    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(screen_width/4.5, screen_height/8,
                        text="Enter Name", font=("Chalkboard SE", 60), fill="black")

    nameEntry = Entry(nameWindow, width=15, justify='center',
                      font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x=screen_width/7, y=screen_height/5.5)

    button = Button(nameWindow, text="Save", font=(
        "Chalkboard SE", 30), width=11, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x=screen_width/6, y=screen_height/4)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def recivedMsg():
    pass


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()


setup()


def gameWindow():
    global playerName
    global canvas1
    global SERVER

    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry('800x600')

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./background.png")

    canvas1 = Canvas(gameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True)
    # Display image
    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(screen_width / 4.5, screen_height / 8, text=f"Welcome {playerName}!", font=("Chalkboard SE", 30),
                        fill="black")

    createTicket()
    placeNumbers()

    gameWindow.resizable(True, True)
    gameWindow.mainloop()


def createTicket():
    global canvas1
    global playerName

    xPos = screen_width / 4
    yPos = screen_height / 4

    mainLabel = Label(canvas1, text=f"{playerName}'s Ticket", font=(
        "Chalkboard SE", 20), bd=5)
    mainLabel.place(x=xPos, y=yPos - 50)

    ticketGrid = []

    for i in range(3):
        rowList = []
        for j in range(9):
            if platform.system() == "Darwin":
                button = Button(canvas1, text=" ", font=("Chalkboard SE", 15), width=3, height=2, bg="yellow",
                                command=lambda i=i, j=j: buttonClick(i, j))
            else:
                button = Button(canvas1, text=" ", font=("Chalkboard SE", 15), width=3, height=2, bg="yellow",
                                command=lambda i=i, j=j: buttonClick(i, j))
            rowList.append(button)
            button.place(x=xPos + j * 50, y=yPos + i * 50)

        ticketGrid.append(rowList)

def placeNumbers():
    global ticketGrid

    randomColList = []
    for _ in range(3):
        randomColList.append(random.sample(range(9), 5))

    for i in range(3):
        randomCol = randomColList[i]
        numberContainer = {k: list(range(k * 10, k * 10 + 10)) for k in randomCol}
        currentNumberList = random.sample(numberContainer[randomCol[0]], 5) + \
                            random.sample(numberContainer[randomCol[1]], 5) + \
                            random.sample(numberContainer[randomCol[2]], 5)

        for j in range(5):
            ticketGrid[i][randomCol[j]].config(text=str(currentNumberList[j]))

def placeNumbers():
    global ticketGrid

    randomColList = []
    for _ in range(3):
        randomColList.append(random.sample(range(9), 5))

    for i in range(3):
        randomCol = randomColList[i]
        
        numberContainer = {k: list(range(k * 10, k * 10 + 10)) for k in range(9)}
        
        currentNumberList = []

        for col in randomCol:
            currentNumberList += random.sample(numberContainer[col], 5)

        for j in range(5):
            ticketGrid[i][randomCol[j]].config(text=str(currentNumberList[j]))