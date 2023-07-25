# Point d'entrée du programme

import List
import Theme
import Word
import random
import pydo
from Pendu import Pendu
from Keyboard import Keyboard
from ActionBar import ActionBar
from tkinter import *


def play():
    # Bouttons de tests de l'affichage du pendu
    complete = pendu.draw()
    print(complete)
    pendu_state = "Rejouer" if complete else "Jouer"
    playButton.configure(text=pendu_state)

# Palette de couleurs
bg_color = '#112233'

# Chemin vers le fichier XML
xml_file = "./data/menus.xml"

# Fenêtre principale
window = Tk()
window.title("Super Pendu 3000")
window.configure(background=bg_color)

# Création de la barre de menus
menu = ActionBar(window, xml_file)

# Création du layout
area_pendu = Canvas(window, background=bg_color, highlightthickness=0)
area_pendu.pack(side=LEFT)
area_info = Canvas(window, background=bg_color, highlightthickness=0)
area_info.pack(side=LEFT)
area_keyboard = Canvas(area_info, background=bg_color, highlightthickness=0)
area_keyboard.pack()
playButton = Button(area_info, text="Jouer", command=play)
playButton.pack()

# Instanciation de l'objet Pendu
pendu = Pendu(area_pendu)

# Instanciation de l'objet Keyboard
clavier = Keyboard(area_keyboard, column=10)

# Rendu de l'application
window.mainloop()
