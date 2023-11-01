from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import os, glob, requests, json, os.path
from tkinter.constants import *
from tkinter.scrolledtext import ScrolledText
from io import BytesIO

searchIndex = 0
searchSize = 0
entryText = ""
searchedJson = []

# Sub functions for buttons inside the 3 different main buttons
def saveButton(request):    
    anime ={
        "Title" : request["data"]["title"],
        "English Title" : request["data"]['title_english'],
        "Cover Art" : request["data"]["images"]["jpg"]["image_url"],
        "Score" : request["data"]["score"],
        "ID" : request["data"]["mal_id"]
    }
    #Creates the JSON file for data storage and checks if the file is created if not then it will create one
    #This saves the programs data even when the program is shut off
    if not (os.path.exists('list.json')):
        with open('list.json', 'w') as f:
            print()
    output = []
    if os.stat('list.json').st_size != 0:                               #Checks if the json file exists if it does read the file and put it in the output array/list    
        with open ('list.json', 'r') as outfile:
            output = json.load(outfile)
    output.append(anime)
    with open ('list.json', 'w') as outfile:
           json.dump(output, outfile, indent = 4)

def saveSearchButton(request):
    anime ={
        "Title" : request["title"],
        "English Title" : request['title_english'],
        "Cover Art" : request["images"]["jpg"]["image_url"],
        "Score" : request["score"],
        "ID" : request["mal_id"]
    }
    #Creates the JSON file for data storage and checks if the file is created if not then it will create one
    #This saves the programs data even when the program is shut off
    if not (os.path.exists('list.json')):
        with open('list.json', 'w') as f:
            print()
    output = []
    if os.stat('list.json').st_size != 0:                               #Checks if the json file exists if it does read the file and put it in the output array/list    
        with open ('list.json', 'r') as outfile:
            output = json.load(outfile)
    output.append(anime)
    with open ('list.json', 'w') as outfile:
           json.dump(output, outfile, indent = 4)    

def clearList(scrollList):
    scrollList.config(state = "normal")
    scrollList.delete('1.0', END)
    scrollList.insert(INSERT, "List is empty.")
    scrollList.config(state = "disabled")
    with open('list.json', 'w') as f:
        print()

def getEntryText(eText):
    global entryText
    global searchIndex
    global searchSize
    global searchedJson

    entryText = eText
    searchIndex = 0
    searchedAnime = entryText.replace(" ", "%20")
    url = "https://api.jikan.moe/v4/anime?q=" + searchedAnime
    respone = requests.get(url)
    searchedJson = respone.json()
    searchSize = len(searchedJson["data"])
    return

def decIndex():
    global searchIndex
    global searchSize
    global searchedJson

    if(searchIndex <= 0):
        searchIndex = searchSize - 1
    else:
        searchIndex -= 1

    while(searchedJson['data'][searchIndex]["rating"] == "Rx - Hentai"):
        searchIndex -= 1
        if(searchIndex <= 0):
            searchIndex = searchSize - 1
            break

def incIndex():
    global searchIndex
    global searchSize
    global searchedJson
    
    searchIndex += 1

    if (searchIndex >= searchSize):
        searchIndex = 0
    
    while(searchedJson['data'][searchIndex]["rating"] == "Rx - Hentai"):
        searchIndex += 1
        if(searchIndex > searchSize):
            searchIndex = 0
            break
    
    


#Fucntions for 3 main buttons
def randomButton():
    random = Tk()
    random.title("AnimeListGUI: Random Anime")
    random.geometry("1000x700")

    respone = requests.get("https://api.jikan.moe/v4/random/anime")
    randomJson = respone.json()
    output = []

    if not (os.path.exists('list.json')):
        with open('list.json', 'w') as f:
            print()

    if os.stat('list.json').st_size != 0:                               #Checks if the json file exists if it does read the file and put it in the output array/list    
        with open ('list.json', 'r') as outfile:
            output = json.load(outfile)
 
    # This will skip all Rx rated animes from showing up in the random selection, also if it is in the list alread
    # This will also check to see if there is a 500 error code, server side, that could not properly fetch the request to get another anime
    while (respone.status_code == 500 or randomJson['data']['rating'] == "Rx - Hentai"  or randomJson["data"]["mal_id"] in output):
        respone = requests.get("https://api.jikan.moe/v4/random/anime")
        randomJson = respone.json()

    img_url = randomJson["data"]["images"]["jpg"]["image_url"]
    imgResponse = requests.get(img_url)
    imgData = imgResponse.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(imgData)))

    enTitle = ""
    jpTitle = ""

    if (randomJson["data"]["title_english"] == None):
        enTitle = randomJson["data"]["title"]
        jpTitle = randomJson["data"]["title"]
    else:
        enTitle = randomJson["data"]["title_english"]
        jpTitle = randomJson["data"]["title"]

    scoreText = ""
    if (randomJson["data"]["score"] == None):
        scoreText ="N/A"
    else:
        scoreText = str(randomJson["data"]["score"]) + "/10"

    label_animeTitle = Label(random, text = enTitle, font =  ('Arial', 18))
    label_jpTitle = Label(random, text = jpTitle, font = ('Arial', 14))
    label_animeImg = Label(random, image = img)
    label_score = Label(random, text = "Score", font = ('Arial', 14))
    label_scoreNum = Label(random, text = scoreText, font = ('Arial', 16, 'bold'))

    button_save = Button(random, text = "Save", height = 3, width = 10, command = lambda: saveButton(randomJson))

    label_search = Label(random, text = "Search for an anime: ")
    entry_searchBar = Entry(random)
    button_search = Button(random, text = "Search", command = lambda: [getEntryText(entry_searchBar.get()), random.destroy(), searchButton()])
    button_list = Button(random, text = "Saved\nAnimes", height = 3, width = 10, command = lambda: [random.destroy(), listButton()])
    button_random = Button(random, text = "Random\nAnime", height = 3, width = 10, command = lambda: [random.destroy(), randomButton()])
    button_airing = Button(random, text = "Airing", height = 3, width = 10, command = lambda: [random.destroy(), airingButton()])

    scrollList = ScrolledText(random, width = 900, height = 13, wrap="word")
    scrollList.pack(side = 'bottom')
    
    label_synopsisTitle = Label(random, text = "Synopsis", font = ('Arial', 14, 'bold'))
    if (randomJson['data']['synopsis'] != None):
        scrollList.insert(INSERT, randomJson["data"]["synopsis"] + '\n')

    label_animeTitle.place(relx = .02, rely = .02, anchor = 'nw')
    label_jpTitle.place(relx = .02, rely = .061, anchor = 'nw')
    label_animeImg.place(relx = .02, rely = .12, anchor = 'nw')

    label_search.place(relx = 0.9, rely = 0.15, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .195, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .195, anchor = 'ne')

    label_score.place(relx = 0.35, rely = 0.25, anchor = 'center')
    label_scoreNum.place(relx = 0.35, rely = 0.29, anchor = 'center')
    
    label_synopsisTitle.place(relx = 0.02, rely = .65, anchor = 'w')
    
    button_random.place(relx = 0.85, rely = 0.325, anchor = 'e')
    button_list.place(relx = 0.85, rely = 0.45, anchor = 'e')
    button_airing.place(relx = 0.85, rely = 0.575, anchor = 'e')
    button_save.place(relx = 0.292, rely = .35)
    
    scrollList.config(state = "disabled")
    # For the random anime button it will just do another fetch request and rewrite the displayed data already shown instead of destroying a window
    # Maybe add a save to list function?
    # pressing the random anime should just replace the labels and images, see comments (make it a function)
    
    random.mainloop()

#Probably going to need scroll wheels on the right side of the screens for both list and airing
# List would show the scores while airing would only show the titles and image (maybe url)
# Add a button to clear the JSON List
def listButton():
    list = Tk()
    list.title("AnimeListGUI: Your List")
    list.geometry("1000x700")

    scrollList = ScrolledText(list, wrap="word")
    scrollList.pack(side = "left", fill = 'both')

    output = []
    imgRef = []
    enTitle = ""
    jpTitle = ""

    if (os.stat("list.json").st_size == 0):
        scrollList.insert(INSERT, "List is empty.")
    else:
        with open ('list.json', 'r') as outfile:
            output = json.load(outfile)

        for data in output:
            img_url = data["Cover Art"]
            imgResponse = requests.get(img_url)
            imgData = imgResponse.content
            img = ImageTk.PhotoImage(Image.open(BytesIO(imgData)))

            imgRef.append(img)

            if(data['English Title'] == None):
                enTitle = data["Title"]
                jpTitle = data["Title"]
            else:
                enTitle = data["English Title"]
                jpTitle = data["Title"]

            scrollList.insert(INSERT, enTitle + '\n' + jpTitle + '\nScore: ' + str(data["Score"]) + '\n')
            scrollList.image_create(INSERT, padx = 5, pady = 5, image = img)
            scrollList.insert(INSERT, '\n\n\n')


    scrollList.config(state = "disabled")

    button_clear = Button(list, text = "Clear", height = 3, width = 10, command = lambda: [clearList(scrollList)])
    button_random = Button(list, text = "Random\nAnime", height = 3, width = 10, command = lambda: [list.destroy(), randomButton()])
    button_airing = Button(list, text = "Airing", height = 3, width = 10, command = lambda: [list.destroy(), airingButton()])

    button_clear.place(relx = 0.9, rely = 0.3, anchor = 'e')
    button_random.place(relx = 0.9, rely = 0.425, anchor = 'e')
    button_airing.place(relx = 0.9, rely = 0.55, anchor = 'e')

    label_search = Label(list, text = "Search for an anime: ")
    entry_searchBar = Entry(list)
    button_search = Button(list, text = "Search", command = lambda: [getEntryText(entry_searchBar.get()), list.destroy(), searchButton()])

    label_search.place(relx = 0.9, rely = 0.01, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .045, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .045, anchor = 'ne')

    list.mainloop()

def airingButton():
    airing = Tk()
    airing.title("AnimeListGUI: Currently Airing Anime")
    airing.geometry("1000x700")

    scrollList = ScrolledText(airing, wrap="word")
    scrollList.pack(side = "left", fill = 'both')

    respone = requests.get("https://api.jikan.moe/v4/seasons/now")
    airingJson = respone.json()
    jsonSize = len(airingJson['data'])

    imgRef = []
    enTitle = ""
    jpTitle = ""

    for x in range(0, jsonSize):
        img_url = airingJson["data"][x]["images"]["jpg"]["image_url"]
        imgResponse = requests.get(img_url)
        imgData = imgResponse.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(imgData)))
        imgRef.append(img)

        if (airingJson["data"][x]["title_english"] == None):
            enTitle = airingJson["data"][x]["title"]
            jpTitle = airingJson["data"][x]["title"]
        else:
            enTitle = airingJson["data"][x]["title_english"]
            jpTitle = airingJson["data"][x]["title"]
        
        scoreText = ""
        if (airingJson["data"][x]["score"] == None):
            scoreText ="N/A"
        else:
            scoreText = str(airingJson["data"][x]["score"]) + "/10"

        scrollList.insert(INSERT, enTitle + '\n' + jpTitle + '\nScore: ' + scoreText + '\n')
        scrollList.image_create(INSERT, padx = 5, pady = 5, image = img)
        scrollList.insert(INSERT, '\n\n\n')

    scrollList.config(state = "disabled")

    button_list = Button(airing, text = "Saved\nAnimes", height = 3, width = 10, command = lambda: [airing.destroy(), listButton()])
    button_random = Button(airing, text = "Random\nAnime", height = 3, width = 10, command = lambda: [airing.destroy(), randomButton()])
    # button_airing = Button(airing, text = "Airing", height = 3, width = 10)

    button_random.place(relx = 0.9, rely = 0.3, anchor = 'e')
    button_list.place(relx = 0.9, rely = 0.425, anchor = 'e')
    # button_airing.place(relx = 0.9, rely = 0.55, anchor = 'e')

    label_search = Label(airing, text = "Search for an anime: ")
    entry_searchBar = Entry(airing)
    button_search = Button(airing, text = "Search", command = lambda: [getEntryText(entry_searchBar.get()), airing.destroy(), searchButton()])

    label_search.place(relx = 0.9, rely = 0.01, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .045, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .045, anchor = 'ne')

    airing.mainloop()

# The search button will have the same layout as the random button and will have an error window if the anime is not found instead of a whole popup screen
# Maybe some next and previous buttons to scroll through a "list"
def searchButton():
    search = Tk()
    search.title("AnimeListGUI: Search")
    search.geometry("1000x700")

    global searchedJson
    global searchIndex

    
    img_url = searchedJson["data"][searchIndex]["images"]["jpg"]["image_url"]
    imgResponse = requests.get(img_url)
    imgData = imgResponse.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(imgData)))

    enTitle = ""
    jpTitle = ""

    if (searchedJson["data"][searchIndex]["title_english"] == None):
        enTitle = searchedJson["data"][searchIndex]["title"]
        jpTitle = searchedJson["data"][searchIndex]["title"]
    else:
        enTitle = searchedJson["data"][searchIndex]["title_english"]
        jpTitle = searchedJson["data"][searchIndex]["title"]

    scoreText = ""
    if (searchedJson["data"][searchIndex]["score"] == None):
        scoreText ="N/A"
    else:
        scoreText = str(searchedJson["data"][searchIndex]["score"]) + "/10"

    label_animeTitle = Label(search, text = enTitle, font =  ('Arial', 18))
    label_jpTitle = Label(search, text = jpTitle, font = ('Arial', 14))
    label_animeImg = Label(search, image = img)
    label_score = Label(search, text = "Score", font = ('Arial', 14))
    label_scoreNum = Label(search, text = scoreText, font = ('Arial', 16, 'bold'))

    button_save = Button(search, text = "Save", height = 3, width = 10, command = lambda: saveSearchButton(searchedJson["data"][searchIndex]))

    label_search = Label(search, text = "Search for an anime: ")
    entry_searchBar = Entry(search)
    button_search = Button(search, text = "Search", command = lambda: [getEntryText(entry_searchBar.get()), search.destroy(), searchButton()])
    button_list = Button(search, text = "Saved\nAnimes", height = 3, width = 10, command = lambda: [search.destroy(), listButton()])
    button_random = Button(search, text = "Random\nAnime", height = 3, width = 10, command = lambda: [search.destroy(), randomButton()])
    button_airing = Button(search, text = "Airing", height = 3, width = 10, command = lambda: [search.destroy(), airingButton()])
    

    scrollList = ScrolledText(search, width = 900, height = 13, wrap="word")
    scrollList.pack(side = 'bottom')
    
    label_synopsisTitle = Label(search, text = "Synopsis", font = ('Arial', 14, 'bold'))
    if (searchedJson['data'][searchIndex]['synopsis'] != None):
        scrollList.insert(INSERT, searchedJson["data"][searchIndex]["synopsis"] + '\n')

    label_animeTitle.place(relx = .02, rely = .02, anchor = 'nw')
    label_jpTitle.place(relx = .02, rely = .061, anchor = 'nw')
    label_animeImg.place(relx = .02, rely = .12, anchor = 'nw')

    label_search.place(relx = 0.9, rely = 0.15, anchor = 'ne')
    entry_searchBar.place(relx = 0.875, rely = .195, anchor = 'ne')
    button_search.place(relx = 0.95, rely = .195, anchor = 'ne')

    label_score.place(relx = 0.35, rely = 0.25, anchor = 'center')
    label_scoreNum.place(relx = 0.35, rely = 0.29, anchor = 'center')
    
    label_synopsisTitle.place(relx = 0.02, rely = .65, anchor = 'w')
    
    button_random.place(relx = 0.85, rely = 0.325, anchor = 'e')
    button_list.place(relx = 0.85, rely = 0.45, anchor = 'e')
    button_airing.place(relx = 0.85, rely = 0.575, anchor = 'e')
    button_save.place(relx = 0.3, rely = .35)

    button_next = Button(search, text = "Next", height = 3, width = 10, command = lambda: [incIndex(), search.destroy(), searchButton()])
    button_previous = Button(search, text = "Prev", height = 3, width = 10, command = lambda: [decIndex(), search.destroy(), searchButton()])

    button_next.place(relx = 0.55, rely = 0.6, anchor = 'center')
    button_previous.place(relx = 0.45, rely = 0.6, anchor = 'center')
    
    scrollList.config(state = "disabled")
    
    search.mainloop()

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
button_list = Button(buttonFrame, text = "Saved\nAnimes", height = 3, width = 10, command = lambda: [root.destroy(), listButton()])
button_random = Button(buttonFrame, text = "Random\nAnime", height = 3, width = 10, command = lambda: [root.destroy(), randomButton()])
button_airing = Button(buttonFrame, text = "Airing", height = 3, width = 10, command = lambda: [root.destroy(), airingButton()])
label_search = Label(entryFrame, text = "Search for an anime: ")
entry_searchBar = Entry(entryFrame)
button_search = Button(entryFrame, text = "Search", command = lambda: [getEntryText(entry_searchBar.get()), root.destroy(), searchButton()])

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