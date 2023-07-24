# Point d'entrée du programme

import List
import Theme
import Word
import random
import pydo
from Pendu import Pendu
from tkinter import *
from tkinter import messagebox


def about():
    "Affichage de la boîte de dialogue 'À propos'"
    messagebox.showinfo(
        "À propos", "Bienvenue dans le jeu du pendu, il est sous licence GNU-GPL 3.0")


def close():
    "Quitter l'application"
    window.destroy()


# Fenêtre principale
window = Tk()
window.title("Super Pendu 3000")

# Création de la barre de menus
menu = Menu(window)

# Création du menu "Fichier"
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="Nouvelle partie", command=None)
menu_file.add_command(label="Choisir une thèmatique", command=None)
menu_file.add_command(label="Choisir une apparence", command=None)
menu_file.add_command(label="Quitter", command=close)
menu.add_cascade(label="Fichier", menu=menu_file)

# Création du menu "Edition"
menu_edit = Menu(menu, tearoff=0)
menu_edit.add_command(label="Éditer les mots", command=None)
menu_edit.add_command(label="Éditer les thématiques", command=None)
menu.add_cascade(label="Édition", menu=menu_edit)

# Création du menu "A propos"
menu_about = Menu(menu, tearoff=0)
menu.add_command(label="À propos", command=about)

# Affichage de la barre de menu
window.config(menu=menu)

# Création du canva du pendu
canva = Canvas(window, background='#112233', height=400, width=400)
canva.pack(side=TOP)

pendu = Pendu(canva)

def play():
    complete = pendu.draw()
    print(complete)
    pendu_state = "Rejouer" if complete else "Jouer"
    playButton.configure(text=pendu_state)

playButton = Button(window, text="Jouer", command=play)
playButton.pack(side=BOTTOM)

window.mainloop()
