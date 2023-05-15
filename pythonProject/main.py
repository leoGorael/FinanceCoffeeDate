import csv
import tkinter as tk
import random
from tkinter import END, TOP, NW, messagebox
from PIL import Image, ImageTk
from subprocess import Popen
import time
import pandas as pd
from pynput.keyboard import Key, Controller





def getWeekcount():
    with open('counter.csv', mode="r+") as infile:
        reader = csv.reader(infile)
        row1 = next(reader)
        return row1[1]


def pop_random(lst):
    if (len(lst) > 1):
        idx = random.randrange(0, len(lst))
        element1 = lst.pop(idx)
        idx2 = random.randrange(0, len(lst))
        element2 = lst.pop(idx2)
        return element1, element2
    else:
        idx = random.randrange(0, len(lst))
        return lst.pop(idx), 'Superpower'


def pop_single(lst):
    if (len(lst) >= 1):
        idx = random.randrange(0, len(lst))
        # print('single',lst)
        element1 = lst.pop(idx)
        return element1
    else:
        return ['Superpower']


def preparePairs():
    teamMembers_apfa = APFA_text.get("1.0", END).split()
    teamMembers_arp = ARP_text.get("1.0", END).split()
    teamMembers_ccpp = CCPP_text.get("1.0", END).split()
    teamMembers_cr = CR_text.get("1.0", END).split()
    teamMembers_ftta = FTTA_text.get("1.0", END).split()
    teamMembers_ica = ICA_text.get("1.0", END).split()
    teamMembers_ifma = IFMA_text.get("1.0", END).split()
    teamMembers_te = TE_text.get("1.0", END).split()

    teee = [teamMembers_apfa, teamMembers_arp, teamMembers_ccpp, teamMembers_cr, teamMembers_ftta, teamMembers_ica,
            teamMembers_ifma, teamMembers_te]

    return teee


def generateCoffeePairs(teams, team_pairs):
    tmp = []

    while teams:
        rand1, rand2 = pop_random(teams)
        if rand2 != 'Superpower':
            while rand1 and rand2:
                p1 = pop_single(rand1)
                p2 = pop_single(rand2)
                team_pairs.append((p1, p2))
                team_pairs.append((p2, p1))

            if len(rand1) > 0:
                tmp.extend([rand1])
            if len(rand2) > 0:
                tmp.extend([rand2])
        else:
            if len(rand1) > 0:
                tmp.extend([rand1])

    if len(tmp) > 1:
        generateCoffeePairs(tmp, team_pairs)
    elif len(tmp) == 1:
        while tmp[0]:
            pp1, pp2 = pop_random(tmp[0])
            team_pairs.append((pp2, pp1))
    else:
        return team_pairs

    return team_pairs


def checkHistory(team_pairs, pair_History):
    pairsLow = [(x.lower(), y.lower()) for x, y in team_pairs]
    pair_HistoryLow = [(x.lower(), y.lower()) for x, y in pair_History]

    if not set(pairsLow).intersection(set(pair_HistoryLow)):
        return True
    else:
        return False


def altElement(pair_List):
    return pair_List[::2]


def execute():
    pair_History = []
    with open('pairs.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            pair_History.append((rows[0], rows[1]))
    prePairs = preparePairs()
    count = 0
    team_pairs = []
    pairs2 = generateCoffeePairs(prePairs, team_pairs)
    checkResult = checkHistory(pairs2, pair_History)
    while (checkResult == False):
        count += 1
        team_pairs = []
        prePairs = preparePairs()
        pairs2 = generateCoffeePairs(prePairs, team_pairs)
        checkResult = checkHistory(pairs2, pair_History)

    write_to_csv(pairs2)
    #print("Count:", count)
    return create_GUI(tk, altElement(pairs2))


def write_to_csv(pairs):
    f = open("pairs.csv", "a", newline="")
    for i in pairs:
        if i[1] != "Superpower":
            writer = csv.writer(f)
            writer.writerow(i)
    f.close()

    f = open("weekreset.csv", "a", newline="")
    writer = csv.writer(f)
    numOfParticipants = (getWeekcount(), str(len(pairs)))
    writer.writerow(numOfParticipants)
    f.close()


def erasePairs():
    answer = tk.messagebox.askyesno(title="Erasing History",
                                    message="Are you sure you want to erase the entire Coffee Date history? This action can not be undone!")
    if answer:
        f = open("pairs.csv", "w+")
        f.close()

        f = open("weekreset.csv", "w+")
        f.close()

        with open('counter.csv', mode="r+", newline='') as infile:
            writer = csv.writer(infile)
            writer.writerow(("count", 0))

        label2.config(text="Week: 0")

def screen_shot():
    keyboard = Controller()
    keyboard.press(Key.alt)
    keyboard.press(Key.print_screen)

    keyboard.release(Key.alt)
    keyboard.release(Key.print_screen)

def create_GUI(tk, pairs):
    button.pack_forget()
    button2.pack_forget()
    label2.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame.pack_forget()

    frame4 = tk.Frame(root, bg='#002e3c')
    frame5 = tk.Frame(root, bg='#002e3c')

    label3 = tk.Label(root, text="Your next Coffee Date is with: \n \n", fg='white', font=('Arial', 20), bg='#002e3c')
    label3.pack()

    frame4.columnconfigure(8, weight=1)
    frame5.columnconfigure(1, weight=1)
    row = 0
    col = 0
    alternate = False
    for p in pairs:
        if row % 2 == 0:
            color = "white"
        else:
            color = "#ffd700"

        if col != 8:
            group1 = tk.Label(frame4, text=p[0] + ' - ' + p[1] , font=('Arial', 16), bg="#002e3c",
                              fg=color)
            group1.grid(row=row, column=col + 1)
            col += 2

        else:
            group1 = tk.Label(frame4, text=p[0]  + ' - ' + p[1], font=('Arial', 16), bg="#002e3c",
                              fg=color)
            group1.grid(row=row, column=8)
            row += 1
            col = 0
        alternate = not alternate

    button4 = tk.Button(frame5, image=copy, bg="#002e3c", border=0, font=('Arial', 20), command=screen_shot)
    button4.grid(row=row+3, column=0)

    frame4.pack()
    frame5.pack()


def loadTeamMembers():
    APFA = pd.read_excel('teammembers.xl'
                         'sx', sheet_name='AP&FA')
    ARP = pd.read_excel('teammembers.xlsx', sheet_name='ARP')
    CCPP = pd.read_excel('teammembers.xlsx', sheet_name='CC&PP')
    CR = pd.read_excel('teammembers.xlsx', sheet_name='CR')
    FTTA = pd.read_excel('teammembers.xlsx', sheet_name='FT&TA')
    ICA = pd.read_excel('teammembers.xlsx', sheet_name='ICA')
    IFMA = pd.read_excel('teammembers.xlsx', sheet_name='IF&MA')
    TE = pd.read_excel('teammembers.xlsx', sheet_name='T&E')

    for index, row in APFA.iterrows():
        APFA_text.insert(END, row[0] + "\n")
    for index, row in ARP.iterrows():
        ARP_text.insert(END, row[0] + "\n")
    for index, row in CCPP.iterrows():
        CCPP_text.insert(END, row[0] + "\n")
    for index, row in CR.iterrows():
        CR_text.insert(END, row[0] + "\n")
    for index, row in FTTA.iterrows():
        FTTA_text.insert(END, row[0] + "\n")
    for index, row in ICA.iterrows():
        ICA_text.insert(END, row[0] + "\n")
    for index, row in IFMA.iterrows():
        IFMA_text.insert(END, row[0] + "\n")
    for index, row in TE.iterrows():
        TE_text.insert(END, row[0] + "\n")


def retrieve_input():
    with open('counter.csv', mode="r+") as infile:
        reader = csv.reader(infile)
        row1 = next(reader)
        count = int(row1[1])
        count += 1

    with open('counter.csv', mode="r+", newline='') as infile:
        writer = csv.writer(infile)
        writer.writerow(("count", count))

    # global LOCALTEAMMEMBERS_APFA, LOCALTEAMMEMBERS_ARP, LOCALTEAMMEMBERS_CCPP, LOCALTEAMMEMBERS_CR, LOCALTEAMMEMBERS_FTTA, LOCALTEAMMEMBERS_ICA, LOCALTEAMMEMBERS_IFMA, LOCALTEAMMEMBERS_TE
    return execute()


def editTeamMembers():
    p = Popen('teammembers.xlsx', shell=True)

    time.sleep(7)
    tk.messagebox.showinfo(title="Closing Program",
                           message="Please reload the program to reflect the changes in the permanent team members!")


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

    image = Image.open('copy.PNG')
    img = image.resize((200, 65))
    copy = ImageTk.PhotoImage(img)


    return reset, magic, logo, editMembers, editHistory, copy


def loadFirstScreen():
    tk.Label(frame, text="AP&FA:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=0, column=0)
    tk.Label(frame, text="ARP:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=0, column=1)
    tk.Label(frame, text="CC&PP:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=0, column=2)
    tk.Label(frame, text="CR:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=0, column=3)
    tk.Label(frame, text="FT&TA:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=2, column=0)
    tk.Label(frame, text="ICA:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=2, column=1)
    tk.Label(frame, text="IF&MA:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=2, column=2)
    tk.Label(frame, text="T&E:", fg='white', font=('Arial', 15), bg='#002e3c').grid(row=2, column=3)

    FTTA_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    FTTA_text.grid(row=3, column=0)

    ICA_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    ICA_text.grid(row=3, column=1)

    IFMA_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    IFMA_text.grid(row=3, column=2)

    TE_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    TE_text.grid(row=3, column=3)

    APFA_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    APFA_text.grid(row=1, column=0)

    ARP_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    ARP_text.grid(row=1, column=1)

    CCPP_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    CCPP_text.grid(row=1, column=2)

    CR_text = tk.Text(frame, width=30, height=15, font=("Arial", 12))
    CR_text.grid(row=1, column=3)

    return FTTA_text, ICA_text, IFMA_text, TE_text, APFA_text, ARP_text, CCPP_text, CR_text


root = tk.Tk()
root.title('Random Coffee Date Generator')
root.config(bg="#002e3c")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

reset, magic, logo, editMembers, editHistory, copy = loadPictures()

label = tk.Label(root, image=logo, bg="#002e3c")
label.pack(side=TOP, anchor=NW, pady=10, padx=10)

label2 = tk.Label(root, text="Week: " + getWeekcount(), fg='white', font=('Arial', 20), bg='#002e3c')
label2.pack()

frame = tk.Frame(root, bg='#002e3c')
frame2 = tk.Frame(root, bg='#002e3c')
frame3 = tk.Frame(root, bg='#002e3c')

frame.columnconfigure(3, weight=1)
frame2.columnconfigure(2, weight=1)
frame3.columnconfigure(0, weight=1)

FTTA_text, ICA_text, IFMA_text, TE_text, APFA_text, ARP_text, CCPP_text, CR_text = loadFirstScreen()
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
