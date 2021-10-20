import requests
from tkinter import *
from tkinter import messagebox

data = None
l1 = []
reqpok = "fish"
def startCatching():
    global data
    global reqpok
    reqpok = input("What pokemon do you want to catch?")
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
    q1 = input("Velg fra dictionaryen hva du vil vite: ")
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

    #if q1 == "abilities":
    #    abilitylist = []
    #    for x in q1output:
    #        print(x)
    #        print()
    #else if q1 == "moves":
    #    print(q1output)
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
    root = Tk()

    root.geometry('600x500')
    photo = PhotoImage(file="pokemon_pics/"+reqpok+".png")
    label = Label(root, image=photo, borderwidth = 3)
    label.pack()
    root.config(bg="red")
    def Take_input():
        INPUT = inputtxt.get("1.0", "end-1c")
        print(INPUT)
        if (INPUT == "120"):
            Output.insert(END, 'Correct')
        else:
            Output.insert(END, "Wrong answer")

    l = Label(text="What is 24 * 5 ? ")
    inputtxt = Text(root, height=5,
                    width=10,
                    bg="white")

    Output = Text(root, height=5,
                  width=25,
                  bg="light cyan")

    Display = Button(root, height=2,
                     width=20,
                     text="Show",
                     command=lambda: Take_input())

    l.pack()
    inputtxt.pack()
    Display.pack()
    Output.pack()
    root.mainloop()




startCatching()



