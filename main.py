import csv
import tkinter as tk
import random
from tkinter import END, TOP, NW, messagebox
from PIL import Image, ImageTk
from subprocess import Popen
import time

def getWeekcount():
    with open('teammembers.csv' ,mode = "r+") as infile:
        reader = csv.reader(infile)
        row1 = next(reader)
        return row1[1]


def pop_random(lst):
    if (len(lst) > 1 ):
        idx = random.randrange(0, len(lst))
        idx2 = random.randrange(0, len(lst)-1)
        return lst.pop(idx), lst.pop(idx2)
    elif (len(lst) == 1):
        idx = random.randrange(0, len(lst))
        return lst.pop(idx)
    else:
        num = random.randrange(1, 10, 1)
        pairString = 'Group {}'.format(num)
        return pairString

def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

def create_pairs(pair_History):
    LOCALTEAMMEMBERS = text.get("1.0", END).split()
    teamMembers = LOCALTEAMMEMBERS

    pairs = []
    while teamMembers:
        rand1, rand2 = pop_random(teamMembers)
        pair = rand1, rand2
        mirror_Pair = rand2, rand1
        pairs.append(pair)
        pairs.append(mirror_Pair)

    if not set(pairs).intersection(set(pair_History)):
        return pairs
    else:
        return False

def altElement(pair_List):
    return pair_List[::2]


def write_to_csv(pairs):
    f = open("pairs.csv", "a", newline="")
    for i in pairs:
        writer = csv.writer(f)
        writer.writerow(i)
    f.close()


def erasePairs():
    f = open("pairs.csv", "w+")
    f.close()

    with open('teammembers.csv', mode="r+",  newline='') as infile:
        writer =csv.writer(infile)
        writer.writerow(("count", 0))

    label2 = tk.Label(root, text="Team Members: (Week: " + getWeekcount() +")", fg='white', font=('Arial', 20), bg='#002e3c')
    label2.pack()

    tk.messagebox.showinfo(title=None, message="Please restart the application!")





def execute():
    pair_History = []
    with open('pairs.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            pair_History.append((rows[0], rows[1]))
    pairs = create_pairs(pair_History)
    while(pairs == False):
        pairs = create_pairs(pair_History)
    write_to_csv(pairs)
    return create_GUI(tk, altElement(pairs))


def create_GUI(tk, pairs):
    text.pack_forget()
    button.pack_forget()
    button2.pack_forget()
    label2.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame.pack_forget()

    frame4 = tk.Frame(root, bg='#002e3c')

    label3 = tk.Label(root, text="Your next Coffee Date is with: \n \n", fg='white', font=('Arial', 20), bg='#002e3c')
    label3.pack()

    frame4.columnconfigure(0, weight=1)
    frame4.columnconfigure(1, weight=1)
    row = 0
    col = 0
    for p in pairs:
        if col == 1:
            group1 = tk.Label(frame4, text=p[0] + ' --- ' + p[1], font=('Arial', 25), bg="#002e3c", fg="white")
            group1.grid(row=row, column=2, sticky=tk.W + tk.E)
            row += 1
            col = 0

        else:
            group1 = tk.Label(frame4, text=p[0] + ' --- ' + p[1] + "\t", font=('Arial', 25), bg="#002e3c", fg="white")
            group1.grid(row=row, column=0, sticky=tk.W + tk.E)
            col += 1

    frame4.pack()


def loadTeamMembers():
    with open('teammembers.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for r in reader:
            if r == []:
                break
            elif r[0] == "count":
                continue
            else:
                text.insert(END, r[0] + "\n")


def retrieve_input():
    with open('teammembers.csv' ,mode = "r+") as infile:
        reader = csv.reader(infile)
        row1 = next(reader)
        print(row1)
        count = int(row1[1])
        count += 1

    with open('teammembers.csv', mode="r+",  newline='') as infile:
        writer =csv.writer(infile)
        writer.writerow(("count", count))


    global LOCALTEAMMEMBERS
    return execute()


def editTeamMembers():
    p = Popen('teammembers.csv', shell=True)


def editDateHistory():
    p = Popen('pairs.csv', shell=True)


def loadPictures():
    image = Image.open('reset.png')
    img = image.resize((200, 50))
    reset = ImageTk.PhotoImage(img)

    image = Image.open('magicButton.png')
    img = image.resize((120, 50))
    magic = ImageTk.PhotoImage(img)

    image = Image.open('logo.png')
    img = image.resize((120, 70))
    logo = ImageTk.PhotoImage(img)

    image = Image.open('editMembers.PNG')
    img = image.resize((150, 55))
    editMembers = ImageTk.PhotoImage(img)

    image = Image.open('editHistory.PNG')
    img = image.resize((150, 55))
    editHistory = ImageTk.PhotoImage(img)

    return reset, magic, logo, editMembers, editHistory

root = tk.Tk()
root.title('Random Coffee Date Generator')
root.config(bg="#002e3c")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))


reset, magic, logo, editMembers, editHistory = loadPictures()

label = tk.Label(root, image=logo, bg="#002e3c")
label.pack(side=TOP, anchor=NW, pady=10, padx=10)

label2 = tk.Label(root, text="Team Members: (Week: " + getWeekcount() +")", fg='white', font=('Arial', 20), bg='#002e3c')
label2.pack()


frame = tk.Frame(root, bg='#002e3c')
frame2 = tk.Frame(root, bg='#002e3c')
frame3 = tk.Frame(root, bg='#002e3c')

frame.columnconfigure(0, weight=1)
frame2.columnconfigure(0, weight=1)
frame2.columnconfigure(1, weight=1)
frame3.columnconfigure(0, weight=1)

text = tk.Text(frame, width=50, height=20, font=("Arial, 12"))
text.grid(row=0, column=0, sticky=tk.W + tk.E)


loadTeamMembers()

button = tk.Button(frame3, image=magic, bg="#002e3c", border=0, font=('Arial', 20), command=retrieve_input)
button.grid(row=0, column=0, sticky=tk.W + tk.E)

button4 = tk.Button(frame2, image=editHistory, bg="#002e3c", border=0, font=('Arial', 20), command=editDateHistory)
button4.grid(row=1, column=0, sticky=tk.W + tk.E)

button3 = tk.Button(frame2, image=editMembers, bg="#002e3c", border=0, font=('Arial', 20), command=editTeamMembers)
button3.grid(row=1, column=1, sticky=tk.W + tk.E)

button2 = tk.Button(frame3, image=reset, bg="#002e3c", border=0, font=('Arial', 20), command=erasePairs)
button2.grid(row=3, column=0, sticky=tk.W + tk.E)

frame.pack()
frame3.pack()
frame2.pack()


root.mainloop()
