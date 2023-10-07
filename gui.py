from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import os

#Fucntions for Buttons
def randomButton():
    root.destroy()
    random = Tk()
    random.title("AnimeListGUI Random")
    random.geometry("1000x700")

    img = ImageTk.PhotoImage(Image.open("Kumodesu.jpg"))

    label_animeTitle = Label(random, text = "So I'm a Spider, So What?", font =  ('Arial', 18))
    label_jpTitle = Label(random, text = "Kumo desu ga, Nani ka?", font = ('Arial', 14))
    label_animeImg = Label(random, image = img)

    label_animeTitle.place(x = 5, y = 5, anchor = 'nw')
    label_jpTitle.place(x = 5, y = 35, anchor = 'nw')
    label_animeImg.place(x = 5, y = 90)
    
    random.mainloop()

def listButton():
    root.destroy()
    list = Tk()
    list.title("AnimeListGUI List")
    list.geometry("1000x700")
    list.mainloop()

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
button_list = Button(buttonFrame, text = "List", height = 3, width = 10, command = listButton)
button_random = Button(buttonFrame, text = "Random", height = 3, width = 10, command = randomButton)
button_airing = Button(buttonFrame, text = "Airing", height = 3, width = 10)
label_search = Label(entryFrame, text = "Search for an anime: ")
entry_searchBar = Entry(entryFrame)
button_search = Button(entryFrame, text = "Submit")

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
Random - show the title, the image, the score, the url, 4-5 similar animes
Airing - Basically the list without the scores (like in progress)
Clear will be a function within the list where you will be able to clear your list
Quit - X button at the top

Search - how do we implement it?
'''


root.mainloop()