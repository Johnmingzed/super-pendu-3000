# Point d'entrée du programme

import List
import Theme
import Word
import random
import pydo
from Pendu import Pendu
from ActionBar import ActionBar
from tkinter import *

# Chemin vers le fichier XML
xml_file = "./data/menus.xml"

# Fenêtre principale
window = Tk()
window.title("Super Pendu 3000")

# Création de la barre de menus
menu = ActionBar(window, xml_file)

# Création du canva du pendu
canva = Canvas(window, background='#112233', height=400, width=400)
canva.pack(side=TOP)

# Instanciation de l'objet Pendu
pendu = Pendu(canva)


def play():
    # Bouttons de tests de l'affichage du pendu
    complete = pendu.draw()
    print(complete)
    pendu_state = "Rejouer" if complete else "Jouer"
    playButton.configure(text=pendu_state)


playButton = Button(window, text="Jouer", command=play)
playButton.pack(side=BOTTOM)

# Rendu de l'application
window.mainloop()
