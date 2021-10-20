import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os.path
from PIL import Image, ImageTk

data = None
l1 = []
reqpok = "fish"
def startCatching():
    global data
    global reqpok
    reqpok = input("What pokemon do you want to catch?")
    if os.path.isfile('pokemon_pics/' + reqpok + '.png') == False:
        startCatching()
    pokeURL = "https://pokeapi.co/api/v2/pokemon/" + reqpok
    requested = requests.get(pokeURL)
    data = requested.json()
    print("You cought a: " + reqpok)
    pokePic = input("Do you want to take a look at your catch?[y/n]")
    if pokePic == "y":
        lookAtPokemon()
    catchPokemon()




def catchPokemon():
    global data
    global l1

    q1dict = data.keys()
    for x in q1dict:
        l1.append(x)
    print(l1)
    askforKnowledge()


def askforKnowledge():
    global data
    global l1
    q1 = input("choose what you want to know: ")
    if q1 in l1:
        q1output = data.get(q1)
    else:
        askforKnowledge()
    if isinstance(q1output, int):
        print(q1output)
    else:
        for x in q1output:
            print(x)
            print()

    moreKnowledge = input("Do you want to know more about this pokemon?[y/n]")
    if moreKnowledge == "y":
        print(l1)
        askforKnowledge()

    else:
        newPokemon = input("do you want to catch a new pokemon?[y/n]")
        if newPokemon == "y":
            startCatching()
        else:
            print("Quitting program")
            return


def lookAtPokemon():
    global reqpok

    def showMega():
        if os.path.isfile('pokemon_megaEvo/' + reqpok + '.png') == True:
            megaPhoto = ImageTk.PhotoImage(Image.open('pokemon_megaEvo/' + reqpok + '.png'))
            label.configure(image=megaPhoto)
            label.photo = megaPhoto

    root = Tk()

    root.geometry('600x500')
    photo = PhotoImage(file="pokemon_pics/"+reqpok+".png")
    label = Label(root, image=photo)
    label.pack()


    buttonMegaEvo = Button(root, text="Show Mega Evolution", command=showMega)
    if os.path.isfile('pokemon_megaEvo/' + reqpok + '.png') == False:
        buttonMegaEvo = Button(root, text=reqpok + " doesnt have a mega")

    exit_button = Button(root, text="Back to pokedex", command=root.destroy)

    buttonMegaEvo.pack()
    exit_button.pack()
    root.mainloop()


startCatching()
