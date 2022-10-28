# AnimeListCLI
## Ver 1.0

This is a side project of mine where I wanted to work with python and APIs in order to better my understanding with python as a programming language and how APIs function in programming. The current version  of this program only allows user to get a random anime from the API and it will append it to a JSON file. This is done so that the data will be stored when the program is shutoff. It also allows the user to print the random anime's aquired as well as clear the list. There is input validation so that there are no duplicates in the list. The last feature of this program is that it will print the currently airing seasonal animes. 

This program was tested and implemented using an Arch Linux installation.

**Dependencies**
The program requires that the `requests` package is installed from the python library, everything else works as intended.

```python -m pip install requests```

The current implentation of this program only works on Linux/MacOS.

Goals to impelemnt

- A way to have users add their own anime to the list
- Add a way for the file to be executed without having to type `python main.py`
