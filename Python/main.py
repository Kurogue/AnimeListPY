#Imports needed for the code to run
#Need to download requests module using pip
import requests
import os
import json
import os.path

#Clears the screen\terminal
os.system("clear")

#Creates the JSON file for data storage and checks if the file is created if not then it will create one
#This saves the programs data even when the program is shut off
if not (os.path.exists('list.json')):
    with open('list.json', 'w') as f:
        print()

#Insert Anime option for the list
#This is the welcome prompt for the animeListCLI program
print("Welcome to AnimeListCLI. Please input \"random\", \"list\", \"airing\", \"clear\" or \"quit\".\nThese choices will give a random anime, your current list of anime, the current anime airing this season, clears the current list, or to quit the program respectively.\nIf you need the options again please type \"help\"\n")

#User input to see what selection they would like
userInput = input("Please input a selection: ")

#An infinite while loop to always get user input until they want to exit the program
while(bool(True)):
    if(userInput.lower() == "random"):
        os.system("clear")
        response = requests.get("https://api.jikan.moe/v4/random/anime")    #Gets the data from the API and stores it
        randomJson = response.json()                                        #Stores the data in a json format
        output = []                                                         #Array/list so that the json file is formatted properly

        if os.stat('list.json').st_size != 0:                               #Checks if the json file exists if it does read the file and put it in the output array/list    
            with open ('list.json', 'r') as outfile:
                output = json.load(outfile)

        #Validation so that it checks if the anime is already in the list the grab a new random anime
        while randomJson["data"]["mal_id"] in output:                           #Checks if the mal_id is already in the json file
            response = requests.get("https://api.jikan.moe/v4/random/anime")    #Grabs a new random anime
            randomJson = response.json()                                        #Stores that new anime in a json format

        #Makes a dictonary with the title, english title, url and mal_id
        anime = {
            "Title" : randomJson["data"]["title"],
            "EnglishTitle" : randomJson["data"]["title_english"],
            "URL" : randomJson["data"]["url"],
            "ID" : randomJson["data"]["mal_id"]
        }

        #Adds the newest entry onto the array/list
        output.append(anime)        

        #Writes the new array/list to the json file with the new entry
        with open ('list.json', 'w') as outfile:    
            json.dump(output, outfile, indent = 4)

        #Printing of the random anime
        print()
        print("Title: " + randomJson["data"]["title"])                      #Prints the title to the user
        if(randomJson["data"]["title_english"] == None):                    #If there is no english title then do not print it
            print("URL: " + randomJson["data"]["url"])                      #Prints the url to the user
        else:
            print("English Title: " + randomJson["data"]["title_english"])  #Prints the english title to the user
            print("URL: " + randomJson["data"]["url"])
        print()
    
    elif(userInput.lower() == "list"):
        os.system("clear")
        output = []                                             #Array/list so that the json file is formatted properly
        print()                                                 #Prints a new line so the input has a new line before printing

        if os.stat('list.json').st_size == 0:                   #If the json file is empty print the list is empty and continue    
            print("\nYour current list is empty")
            userInput = input("Please input a selection: ")     #Prevents infinite loop
            continue

        with open ('list.json', 'r') as outfile:                #Opens the json file of anime entries to read
            output = json.load(outfile)                         #Puts the json file into an array/list

        for data in output:
            print("Title: " + data["Title"])                     #Prints the Title to the user
            if(data["EnglishTitle"] == None):                    #If there is no english title then do not print it
                print("URL: " + data["URL"])                     #Prints the url to the user
            else:
                print("English Title: " + data["EnglishTitle"])  #Prints the english title to the user
                print("URL: " + data["URL"])
            print()
    
    elif(userInput.lower() == "airing"):
        os.system("clear")
        response = requests.get("https://api.jikan.moe/v4/seasons/now")     #Gets the data from the API and stores it 
        airingJson = response.json()                                        #Stores the data in a json format
        jsonSize = len(airingJson["data"])                                  #Gets the size of the json file with the data keys
        print()
        for x in range(0, jsonSize):                                        #For loop to loop through all the data keys in the json file
            print("Title: " + airingJson["data"][x]["title"])               #Prints the title of the anime
            if(airingJson["data"][x]["title_english"] == None):             #If the english title does not exist then skip it
                print("URL: " + airingJson["data"][x]["url"])               #Prints the url for the anime
            else:
                print("English Title: " + airingJson["data"][x]["title_english"])   #Prints the english title if there is one
                print("URL: " + airingJson["data"][x]["url"])
            print()
    
    elif(userInput.lower() == "clear"):
        os.system("clear")
        with open('list.json', 'w') as f:       #Opens a new file called list.json
            print()                             #Prints an empty string to it
    
    elif(userInput.lower() == "quit" or userInput.lower() == "exit"):
        os.system("clear")
        exit()          #exits the program
    
    elif(userInput.lower() == "help"):
        os.system("clear")
        print("\nrandom = Random Anime\nlist = Current Anime List\nairing = Current Airing Anime\nclear = Clears the Current Anime List\nquit = Quits the Program\nhelp = Gives Options Again")

    print("Please input \"random\", \"list\", \"airing\", \"clear\", \"quit\" or \"help\"")     #Prints out the options again for the user to select
    userInput = input("Please input a selection: ")                                             #Gets user input for the next selection so that there is no infinite loop
