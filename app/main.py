# Point d'entrée du programme

import List
import Theme
import Word
import random
import pydo
from Pendu import Pendu
from DisplayWord import DisplayWord
from Keyboard import Keyboard
from ActionBar import ActionBar
from tkinter import *
from tkinter import messagebox


def main():

    # Palette de couleurs
    bg_color = '#112233'

    # Fenêtre principale
    window = Tk()
    window.title("Super Pendu 3000")
    window.configure(background=bg_color)

    def play(e):
        # Bouttons de tests de l'affichage du pendu
        if not gameover():
            if not display.victory:
                key = e.char
                if not display.testLetter(key):
                    pendu.draw()
                display.display()
                gameover()

    def gameover():
        if pendu.complete:
            print('Vous avez perdu...')
            return 1
        else:
            return 0

    def newgame():
        print('Nouvelle partie')

    def about():
        "Affichage de la boîte de dialogue 'À propos'"
        messagebox.showinfo(
            "À propos", "Bienvenue dans le jeu du pendu, il est sous licence GNU-GPL 3.0")

    def close():
        "Quitter l'application"
        window.destroy()


    # Chemin vers le fichier XML
    xml_file = "./data/menus.xml"


    # Création de la barre de menus
    menu = ActionBar(window, xml_file)

    # Création du layout
    layout = Canvas(window, background=bg_color, highlightthickness=0)
    layout.pack(expand=1)
    area_pendu = Canvas(layout, background=bg_color, highlightthickness=0)
    area_pendu.pack(side=LEFT)
    area_info = Canvas(layout, background=bg_color, highlightthickness=0)
    area_info.pack(side=LEFT)
    area_word = Canvas(area_info, background=bg_color, highlightthickness=0)
    area_word.pack(side=TOP)
    area_keyboard = Canvas(
        area_info, background=bg_color, highlightthickness=0)
    area_keyboard.pack(side=BOTTOM)

    # Instanciation de l'objet Pendu
    pendu = Pendu(area_pendu)

    # Instanciation de l'objet Keyboard
    clavier = Keyboard(area_keyboard, column=10)

    # Instanciation du l'objet Displayword
    display = DisplayWord(area_word, 'polymorphisme')

    # Tentative du joueur
    window.bind('<Key>', play)

    # Rendu de l'application
    window.mainloop()


if __name__ == "__main__":
    main()
