from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import os, glob
from tkinter.constants import *
from tkinter.scrolledtext import ScrolledText

#Fucntions for Buttons
def randomButton():
    random = Tk()
    random.title("AnimeListGUI: Random Anime")
    random.geometry("1000x700")

    img = ImageTk.PhotoImage(Image.open("Kumodesu.jpg"))
    rec1 = Image.open("slime.jpg")
    rec1 = rec1.resize((70, 100))
    rec1 = ImageTk.PhotoImage(rec1)
    rec2 = Image.open("overlord.jpg")
    rec2 = rec2.resize((70, 100))
    rec2 = ImageTk.PhotoImage(rec2)

    label_animeTitle = Label(random, text = "So I'm a Spider, So What?", font =  ('Arial', 18))
    label_jpTitle = Label(random, text = "Kumo desu ga, Nani ka?", font = ('Arial', 14))
    label_animeImg = Label(random, image = img)
    label_search = Label(random, text = "Search for an anime: ")
    entry_searchBar = Entry(random)
    button_search = Button(random, text = "Search")
    label_score = Label(random, text = "Score", font = ('Arial', 14))
    label_scoreNum = Label(random, text = "7.4/10", font = ('Arial', 16, 'bold'))
    button_list = Button(random, text = "List", height = 3, width = 10, command = lambda: [random.destroy(), listButton()])
    button_random = Button(random, text = "Random", height = 3, width = 10)
    button_airing = Button(random, text = "Airing", height = 3, width = 10, command = lambda: [random.destroy(), airingButton()])
    label_rec = Label(random, text = "Recommendations", font = ('Arial', 14, 'bold'))
    label_rec1 = Label(random, image = rec1, width = 70, height = 100)
    label_rec1Score = Label(random, text = "That Time I Got Reincarnated as a Slime\nScore: 8.14 / 10", font = ('Arial', 12))
    label_rec2 = Label(random, image = rec2, width = 70, height = 100)
    label_rec2Score = Label(random, text = "Overlord\nScore: 7.91 / 10", font = ('Arial', 12))

    label_animeTitle.place(relx = .02, rely = .02, anchor = 'nw')
    label_jpTitle.place(relx = .02, rely = .061, anchor = 'nw')
    label_animeImg.place(relx = .02, rely = .12, anchor = 'nw')
    label_search.place(relx = 0.9, rely = 0.01, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .045, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .045, anchor = 'ne')
    label_score.place(relx = 0.35, rely = 0.25, anchor = 'center')
    label_scoreNum.place(relx = 0.35, rely = 0.29, anchor = 'center')
    label_rec.place(relx = .02, rely = .65, anchor = 'sw')

    label_rec1.place(relx = 0.02, rely = .81, anchor = 'sw')
    label_rec1Score.place(relx = 0.12, rely = .75, anchor = 'sw')
    label_rec2.place(relx = 0.02, rely = .975, anchor = 'sw')
    label_rec2Score.place(relx = 0.12, rely = .925, anchor = 'sw')
    
    button_random.place(relx = 0.85, rely = 0.225, anchor = 'e')
    button_list.place(relx = 0.85, rely = 0.35, anchor = 'e')
    button_airing.place(relx = 0.85, rely = 0.475, anchor = 'e')
    
    # For the random anime button it will just do another fetch request and rewrite the displayed data already shown instead of destroying a window
    # Maybe add a save to list function?
    # pressing the random anime should just replace the labels and images, see comments (make it a function)

    
    random.mainloop()

#Probably going to need scroll wheels on the right side of the screens for both list and airing
# List would show the scores while airing would only show the titles and image (maybe url)
def listButton():
    list = Tk()
    list.title("AnimeListGUI: Your List")
    list.geometry("1000x700")

    scrollList = ScrolledText(list)
    scrollList.pack(side = "left", fill = 'both')

    #Retrive them from a json file then store them into lists or smt
    imgList = ["tengoku.jpg", "Kumodesu.jpg", "overlord.jpg", "slime.jpg"]
    titleEN = ['Heavenly Dillusion', "So I\'m a Spider, So What?", "Overlord", "That Time I Got Reincarnated as a Slime"]
    titleJP = ["Tengoku Daimakyou", "Kumo Desu ga, Nani ka?", "", "Tensei shitara Slime Datta Ken"]
    scores = ["8.2/10", "7.45", "7.9/10", "8.1/10"]

    imgRef = []

    count = 0
    for x in imgList:
        img = Image.open(x)
        img = ImageTk.PhotoImage(img)
        imgRef.append(img)

        scrollList.insert(INSERT, titleEN[count] + '\n' + titleJP[count] + '\nScore: ' + scores[count] + '\n')
        scrollList.image_create(INSERT, padx = 5, pady = 5, image = img)
        scrollList.insert(INSERT, '\n\n\n')
        count+=1

    scrollList.config(state = "disabled")

    # button_list = Button(list, text = "List", height = 3, width = 10)
    button_random = Button(list, text = "Random", height = 3, width = 10, command = lambda: [list.destroy(), randomButton()])
    button_airing = Button(list, text = "Airing", height = 3, width = 10, command = lambda: [list.destroy(), airingButton()])

    button_random.place(relx = 0.9, rely = 0.3, anchor = 'e')
    # button_list.place(relx = 0.9, rely = 0.425, anchor = 'e')
    button_airing.place(relx = 0.9, rely = 0.425, anchor = 'e')

    label_search = Label(list, text = "Search for an anime: ")
    entry_searchBar = Entry(list)
    button_search = Button(list, text = "Search")

    label_search.place(relx = 0.9, rely = 0.01, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .045, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .045, anchor = 'ne')

    list.mainloop()

def airingButton():
    airing = Tk()
    airing.title("AnimeListGUI: Currently Airing Anime")
    airing.geometry("1000x700")

    scrollList = ScrolledText(airing)
    scrollList.pack(side = "left", fill = 'both')

    #Retrive them from a json file then store them into lists or smt
    imgList = ["spyFam.jpg", "tate.jpg", "frieren.jpg", "stone.jpg", "undead.jpg"]
    titleEN = ['Spy x Family Season 2', "The Rising of the Shield Hero Season 3", "Frieren: Beyond Journey's End", "Dr. Stone: New World Part 2", "Undead Unluck"]
    titleJP = ["", "Tate no Yuusha no Nariagari Season 3", "Sousou no Frieren", "", ""]
    scores = ["8.5/10", "7.7", "8.9/10", "N/A", "8.1/10"]

    imgRef = []

    count = 0
    for x in imgList:
        img = Image.open(x)
        img = ImageTk.PhotoImage(img)
        imgRef.append(img)

        scrollList.insert(INSERT, titleEN[count] + '\n' + titleJP[count] + '\nScore: ' + scores[count] + '\n')
        scrollList.image_create(INSERT, padx = 5, pady = 5, image = img)
        scrollList.insert(INSERT, '\n\n\n')
        count+=1

    scrollList.config(state = "disabled")

    button_list = Button(airing, text = "List", height = 3, width = 10, command = lambda: [airing.destroy(), listButton()])
    button_random = Button(airing, text = "Random", height = 3, width = 10, command = lambda: [airing.destory(), randomButton()])
    # button_airing = Button(airing, text = "Airing", height = 3, width = 10)

    button_random.place(relx = 0.9, rely = 0.3, anchor = 'e')
    button_list.place(relx = 0.9, rely = 0.425, anchor = 'e')
    # button_airing.place(relx = 0.9, rely = 0.55, anchor = 'e')

    label_search = Label(airing, text = "Search for an anime: ")
    entry_searchBar = Entry(airing)
    button_search = Button(airing, text = "Search")

    label_search.place(relx = 0.9, rely = 0.01, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .045, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .045, anchor = 'ne')

    airing.mainloop()

#GUI itself
root = Tk()
root.title("AnimeListGUI")
root.geometry("1000x700")

#Frames
buttonFrame = Frame(root)
entryFrame = Frame(root)
entryFrame.pack(side = 'bottom', fill = X, pady = (0, 50))
buttonFrame.pack (side = 'bottom', fill = X, pady = (0, 50))

#Fonts
titleFont = tkFont.Font(size = 26)
descriptionFont = tkFont.Font(size = 14)

#Items to populate the frames and GUI
label_Title = Label(root)
label_description = Label(root)
button_list = Button(buttonFrame, text = "List", height = 3, width = 10, command = lambda: [root.destroy(), listButton()])
button_random = Button(buttonFrame, text = "Random", height = 3, width = 10, command = lambda: [root.destroy(), randomButton()])
button_airing = Button(buttonFrame, text = "Airing", height = 3, width = 10, command = lambda: [root.destroy(), airingButton()])
label_search = Label(entryFrame, text = "Search for an anime: ")
entry_searchBar = Entry(entryFrame)
button_search = Button(entryFrame, text = "Search")

#Placing the items into the frames/GUI
label_Title.pack(pady = (100, 20))
label_description.pack()
button_list.pack(in_=buttonFrame, side = "left", padx = (300, 10)) #side = 'bottom'
button_random.pack(in_=buttonFrame, side = "left", padx = 10)
button_airing.pack(in_=buttonFrame, side = "left", padx = (10, 0))
label_search.pack(side = 'left', padx = (290, 0))
entry_searchBar.pack(side = 'left')
button_search.pack(side = 'left', padx = (5))

label_Title.config(font = titleFont, text = "Welcome to AnimeListGUI.")
label_description.config(font = descriptionFont, text = "Welcome to AnimeListGUI, in this program it will allow you to find random animes. \nThere is also a search function for you to find any anime you had a question about.\nTo get started hit the random button for your first random anime.")

'''
USE PLACE FOR THE OTHER WINDOWS 

List - show the title, the image, the score and the url to the mal (should you be able to see the recommended anime here?)
    The recommendations would show the title of the show, the score and the image of it

Random - show the title, the image, the score, the url, 4-5 similar animes

Airing - Basically the list without the scores (like in progress)

Clear will be a function within the list where you will be able to clear your list

Quit - X button at the top

Search - how do we implement it? (Back end problem)
'''


root.mainloop()