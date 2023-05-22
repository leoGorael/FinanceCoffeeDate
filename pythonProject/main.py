import csv
import tkinter as tk
import random
import webbrowser

import pandas as pd
from tkinter import END, TOP, NW, messagebox
from PIL import Image, ImageTk
from subprocess import Popen
from pynput.keyboard import Key, Controller


def getWeekcount():
    with open('data/counter.csv', mode="r+") as infile:
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

        element1 = lst.pop(idx)
        return element1
    else:
        return ['Superpower']


def preparePairs():
    teamMembers_apfa = list(filter(None, (APFA_text.get("1.0", END).split('\n'))))
    teamMembers_arp = list(filter(None, (ARP_text.get("1.0", END).split('\n'))))
    teamMembers_ccpp = list(filter(None, (CCPP_text.get("1.0", END).split('\n'))))
    teamMembers_cr = list(filter(None, (CR_text.get("1.0", END).split('\n'))))
    teamMembers_ftta = list(filter(None, (FTTA_text.get("1.0", END).split('\n'))))
    teamMembers_ica = list(filter(None, (ICA_text.get("1.0", END).split('\n'))))
    teamMembers_ifma = list(filter(None, (IFMA_text.get("1.0", END).split('\n'))))
    teamMembers_te = list(filter(None, (TE_text.get("1.0", END).split('\n'))))

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
    with open('data/pairs.csv', mode='r') as infile:
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
    return create_GUI(tk, altElement(pairs2))


def write_to_csv(pairs):
    f = open("data/pairs.csv", "a", newline="")
    for i in pairs:
        if i[1] != "Superpower":
            writer = csv.writer(f)
            writer.writerow(i)
    f.close()

    f = open("data/weekreset.csv", "a", newline="")
    writer = csv.writer(f)
    numOfParticipants = (getWeekcount())
    writer.writerow(numOfParticipants)
    f.close()


def erasePairs():
    answer = tk.messagebox.askyesno(title="Erasing History",
                                    message="Are you sure you want to erase the entire Coffee Date history? This action can not be undone!")
    if answer:
        f = open("data/pairs.csv", "w+")
        f.close()

        f = open("data/weekreset.csv", "w+")
        f.close()

        with open('data/counter.csv', mode="r+", newline='') as infile:
            writer = csv.writer(infile)
            writer.writerow(("count", 0))

        labelWeekCount.config(text="Week: 0")


def screen_shot():
    keyboard = Controller()
    keyboard.press(Key.alt)
    keyboard.press(Key.print_screen)
    keyboard.release(Key.alt)
    keyboard.release(Key.print_screen)


def showLastWeek():
    lastPairs = []
    with open('data/lastPair.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            lastPairs.append((rows[0], rows[1]))

    create_GUI(tk, lastPairs)


def create_GUI(tk, pairs):
    labelWeekCount.pack_forget()
    buttonsFrame.pack_forget()
    executeButtonFrame.pack_forget()
    mainFrame.pack_forget()
    frameContact.pack_forget()


    frame4 = tk.Frame(root, bg='#002e3c')
    frame5 = tk.Frame(root, bg='#002e3c')

    tk.Label(root, text="Your next Coffee Date is with: \n \n", fg='white', font=('Arial', 20), bg='#002e3c').pack()

    row = 0
    col = 0
    alternate = False
    for p in pairs:
        if row % 2 == 0:
            color = "white"
        else:
            color = "#ffd700"

        if col != 8:
            tk.Label(frame4, text=p[0][0:15] + ' - ' + p[1][0:15], font=('Arial', 12, 'bold'), bg="#002e3c",
                     fg=color).grid(row=row, column=col + 1)
            col += 2
        else:
            tk.Label(frame4, text=p[0][0:15] + ' - ' + p[1][0:15], font=('Arial', 12, 'bold'), bg="#002e3c",
                     fg=color).grid(row=row, column=8)
            row += 1
            col = 0
        alternate = not alternate

    tk.Label(frame4, bg="#002e3c").grid(row=row + 1, column=0)
    tk.Button(frame5, image=copy, bg="#002e3c", border=0, font=('Arial', 20), command=screen_shot).grid(row=row + 2,
                                                                                                        column=0)
    frame4.pack()
    frame5.pack()

    f = open("data/lastPair.csv", "w", newline="")
    for i in pairs:
        writer = csv.writer(f)
        writer.writerow(i)
    f.close()


def loadTeamMembers(FTTA_text, ICA_text, IFMA_text, TE_text, APFA_text, ARP_text, CCPP_text, CR_text):
    APFA = pd.read_excel('data/pallteammembers.xlsx', sheet_name='AP&FA')
    ARP = pd.read_excel('data/pallteammembers.xlsx', sheet_name='ARP')
    CCPP = pd.read_excel('data/pallteammembers.xlsx', sheet_name='CC&PP')
    CR = pd.read_excel('data/pallteammembers.xlsx', sheet_name='CR')
    FTTA = pd.read_excel('data/pallteammembers.xlsx', sheet_name='FT&TA')
    ICA = pd.read_excel('data/pallteammembers.xlsx', sheet_name='ICA')
    IFMA = pd.read_excel('data/pallteammembers.xlsx', sheet_name='IF&MA')
    TE = pd.read_excel('data/pallteammembers.xlsx', sheet_name='T&E')

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
    with open('data/counter.csv', mode="r+") as infile:
        reader = csv.reader(infile)
        row1 = next(reader)
        count = int(row1[1])
        count += 1

    with open('data/counter.csv', mode="r+", newline='') as infile:
        writer = csv.writer(infile)
        writer.writerow(("count", count))

    return execute()


def editTeamMembers():
    answer = tk.messagebox.askokcancel(title="Reload Application",
                                       message="Please reload the program if changes are made to the teammembers to reflect the permanent changes!")
    if answer:
        Popen('data\pallteammembers.xlsx', shell=True)


def editDateHistory():
    Popen('data\pairs.csv', shell=True)


def loadPictures():
    magic = ImageTk.PhotoImage(Image.open('icons/magicButton6.png').resize((250, 55)))
    reset = ImageTk.PhotoImage(Image.open('icons/reset.png').resize((300, 55)))
    logofull = ImageTk.PhotoImage(Image.open('icons/logofull.png').resize((600, 70)))
    editMembers = ImageTk.PhotoImage(Image.open('icons/editMembers.PNG').resize((300, 55)))
    editHistory = ImageTk.PhotoImage(Image.open('icons/editHistory.PNG').resize((300, 55)))
    copy = ImageTk.PhotoImage(Image.open('icons/copy.PNG').resize((300, 55)))
    last = ImageTk.PhotoImage(Image.open('icons/last.png').resize((300, 55)))
    design = ImageTk.PhotoImage(Image.open('icons/design.png').resize((55, 55)))

    return reset, magic, editMembers, editHistory, copy, last, logofull, design

def showDeveloper():
    answer = tk.messagebox.askyesno('Contact Information', 'If you have any questions or concerns regarding the application please contact Linard Gorael Sinabak.\nDo you wish to reach out?')
    if answer:
        webbrowser.open('https://www.linkedin.com/in/linard-gorael-sinabak/')

def loadTeamPictures():
    apfa = ImageTk.PhotoImage(Image.open('teams/apfa.png').resize((120, 30)))
    arp = ImageTk.PhotoImage(Image.open('teams/arp.png').resize((120, 30)))
    ccpp = ImageTk.PhotoImage(Image.open('teams/ccpp.png').resize((120, 30)))
    cr = ImageTk.PhotoImage(Image.open('teams/cr.png').resize((120, 30)))
    ftta = ImageTk.PhotoImage(Image.open('teams/ftta.png').resize((120, 30)))
    ica = ImageTk.PhotoImage(Image.open('teams/ica.png').resize((120, 30)))
    ifma = ImageTk.PhotoImage(Image.open('teams/ifma.png').resize((120, 30)))
    te = ImageTk.PhotoImage(Image.open('teams/te.png').resize((120, 30)))

    return apfa, arp, ccpp, cr, ftta, ica, ifma, te


def loadFirstScreen(mainFrame):
    tk.Label(mainFrame, image=apfa, bg="#002e3c").grid(row=0, column=0)
    tk.Label(mainFrame, image=arp, bg="#002e3c").grid(row=0, column=2)
    tk.Label(mainFrame, image=ccpp, bg="#002e3c").grid(row=0, column=4)
    tk.Label(mainFrame, image=cr, bg="#002e3c").grid(row=0, column=6)
    tk.Label(mainFrame, image=ftta, bg="#002e3c").grid(row=2, column=0)
    tk.Label(mainFrame, image=ica, bg="#002e3c").grid(row=2, column=2)
    tk.Label(mainFrame, image=ifma, bg="#002e3c").grid(row=2, column=4)
    tk.Label(mainFrame, image=te, bg="#002e3c").grid(row=2, column=6)

    tk.Label(mainFrame, bg='#002e3c').grid(row=0, column=1)
    tk.Label(mainFrame, bg='#002e3c').grid(row=0, column=3)
    tk.Label(mainFrame, bg='#002e3c').grid(row=0, column=5)

    FTTA_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    FTTA_text.grid(row=3, column=0)

    ICA_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    ICA_text.grid(row=3, column=2)

    IFMA_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    IFMA_text.grid(row=3, column=4)

    TE_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    TE_text.grid(row=3, column=6)

    APFA_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    APFA_text.grid(row=1, column=0)

    ARP_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    ARP_text.grid(row=1, column=2)

    CCPP_text = tk.Text(mainFrame, width=22, height=12, font=("Gotham", 12, 'bold'), background="#f1efed")
    CCPP_text.grid(row=1, column=4)

    CR_text = tk.Text(mainFrame, width=22, height=12, font=("Arial", 12, 'bold'), background="#f1efed")
    CR_text.grid(row=1, column=6)

    loadTeamMembers(FTTA_text, ICA_text, IFMA_text, TE_text, APFA_text, ARP_text, CCPP_text, CR_text)

    return FTTA_text, ICA_text, IFMA_text, TE_text, APFA_text, ARP_text, CCPP_text, CR_text


def loadButtons(executeButtonFrame, buttonsFrame, frameContact):
    tk.Button(executeButtonFrame, image=magic, bg="#002e3c", border=0, command=retrieve_input).grid(row=1, column=0)
    tk.Button(buttonsFrame, image=reset, bg="#002e3c", border=0, command=erasePairs).grid(row=2, column=0)
    tk.Button(buttonsFrame, image=last, bg="#002e3c", border=0, command=showLastWeek).grid(row=2, column=2)
    tk.Button(buttonsFrame, image=editHistory, bg="#002e3c", border=0, command=editDateHistory).grid(row=4, column=0)
    tk.Button(buttonsFrame, image=editMembers, bg="#002e3c", border=0, command=editTeamMembers).grid(row=4, column=2)
    tk.Button(frameContact, image=design, bg="#002e3c", border=0, command=showDeveloper).grid(row=0, column=1)
    tk.Label(frameContact, bg="#002e3c", text="\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t").grid(row=0, column=0)

    tk.Label(executeButtonFrame, bg="#002e3c").grid(row=0, column=0)
    tk.Label(buttonsFrame, bg="#002e3c").grid(row=4, column=1)
    tk.Label(buttonsFrame, bg="#002e3c").grid(row=2, column=1)


def loadHeader(root):
    tk.Label(root, image=logofull, bg="#002e3c").pack(side=TOP, anchor=NW, pady=10, padx=10)
    labelWeekCount = tk.Label(root, text="Week: " + getWeekcount(), fg='white', font=('Arial', 16, 'bold'),
                              bg='#002e3c')
    labelWeekCount.pack()

    return labelWeekCount


root = tk.Tk()
root.title('Random Coffee Date Generator')
root.config(bg="#002e3c")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

mainFrame = tk.Frame(root, bg='#002e3c')
executeButtonFrame = tk.Frame(root, bg='#002e3c')
buttonsFrame = tk.Frame(root, bg='#002e3c')
frameContact = tk.Frame(root, bg='#002e3c')

reset, magic, editMembers, editHistory, copy, last, logofull, design = loadPictures()
apfa, arp, ccpp, cr, ftta, ica, ifma, te = loadTeamPictures()
FTTA_text, ICA_text, IFMA_text, TE_text, APFA_text, ARP_text, CCPP_text, CR_text = loadFirstScreen(mainFrame)

labelWeekCount = loadHeader(root)
loadButtons(executeButtonFrame, buttonsFrame, frameContact)

mainFrame.pack()
executeButtonFrame.pack()
buttonsFrame.pack()
frameContact.pack()

root.mainloop()
