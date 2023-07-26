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


class Main():

    def __init__(self) -> None:

        # Palette de couleurs
        bg_color = '#112233'

        # Fenêtre principale
        self.window = Tk()
        self.window.title("Super Pendu 3000")
        self.window.configure(background=bg_color)

        # Chemin vers le fichier XML
        self.xml_file = "./data/menus.xml"


        # Création du layout
        self.layout = Canvas(self.window, background=bg_color, highlightthickness=0)
        self.layout.pack(expand=1)
        self.area_pendu = Canvas(self.layout, background=bg_color, highlightthickness=0)
        self.area_pendu.pack(side=LEFT)
        self.area_info = Canvas(self.layout, background=bg_color, highlightthickness=0)
        self.area_info.pack(side=LEFT)
        self.area_word = Canvas(self.area_info, background=bg_color,
                           highlightthickness=0)
        self.area_word.pack(side=TOP)
        self.area_keyboard = Canvas(
            self.area_info, background=bg_color, highlightthickness=0)
        self.area_keyboard.pack(side=BOTTOM)

        self.newgame()

    def newgame(self):
        print("Initialisation d'une nouvelle partie")

        # Création de la barre de menus
        menu = ActionBar(self.window, self.xml_file, self)

        # Instanciation de l'objet Pendu
        self.pendu = Pendu(self.area_pendu)

        # Instanciation de l'objet Keyboard
        self.clavier = Keyboard(self.area_keyboard, column=10)

        # Instanciation du l'objet Displayword
        self.display = DisplayWord(self.area_word, 'polymorphisme')

        # Tentative du joueur
        self.window.bind('<Key>', self.play)

        # Rendu de l'application
        self.window.mainloop()

    def play(self, e):
        # Bouttons de tests de l'affichage du pendu
        if not self.gameover():
            if not self.display.victory:
                key = e.char
                if not self.display.testLetter(key):
                    self.pendu.draw()
                self.display.display()
                self.gameover()

    def gameover(self):
        if self.pendu.complete:
            print('Vous avez perdu...')
            return 1
        else:
            return 0


    def about(self):
        "Affichage de la boîte de dialogue 'À propos'"
        messagebox.showinfo(
            "À propos", "Bienvenue dans le jeu du pendu, il est sous licence GNU-GPL 3.0")

    def close(self):
        "Quitter l'application"
        self.window.destroy()


if __name__ == "__main__":
    main = Main()
