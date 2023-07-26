# Point d'entrée du programme

import List
import Theme
import Word
import random
import pydo
from Config import Config
from Pendu import Pendu
from DisplayWord import DisplayWord
from Keyboard import Keyboard
from ActionBar import ActionBar
from tkinter import *
from tkinter import messagebox
import string


class Main():

    def __init__(self) -> None:

        # Chemin vers les fichiers de configuration
        self.xml_file = "./data/menus.xml"
        self.json_file = "./data/conf.json"

        # Chargement du fichier de configuration
        self.config = Config(self.json_file).toDict()

        # Palette de couleurs
        bg_color = self.config['canevas']

        # Fenêtre principale
        self.window = Tk()
        self.window.title("Super Pendu 3000")
        self.window.configure(background=bg_color)

        # Création du layout
        self.layout = Canvas(
            self.window, background=bg_color, highlightthickness=0)
        self.layout.pack(expand=1)
        self.area_pendu = Canvas(
            self.layout, background=bg_color, highlightthickness=0)
        self.area_pendu.pack(side=LEFT)
        self.area_info = Canvas(
            self.layout, background=bg_color, highlightthickness=0)
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
        self.pendu = Pendu(self.area_pendu, self.config)

        # Instanciation de l'objet Keyboard
        self.clavier = Keyboard(self.area_keyboard, self.config, column=10)

        # Instanciation du l'objet Displayword
        self.display = DisplayWord(
            self.area_word, 'polymorphisme', self.config)

        # Tentative du joueur
        self.window.bind('<Key>', self.keyPlay)
        self.window.bind('<Button>', self.mousePlay)

        # Rendu de l'application
        self.window.mainloop()

    def keyPlay(self, e):
        if not self.gameover() and not self.display.victory and e.char:
            # On vérifie que la touche entrée correspont à un caractère
            key = e.char
            print("Clavier input :", key, "Event :", e)
            if key in string.ascii_letters:
                self.play(key)

    def mousePlay(self, e):
        if not self.gameover() and not self.display.victory:
            target_id = self.area_keyboard.find_closest(e.x, e.y)
            target_tags = self.area_keyboard.gettags(target_id)
            if len(target_tags) == 2:
                if target_tags[1] == 'current':
                    letter = target_tags[0]
                    self.play(letter)

    def play(self, key):
        if not self.display.testLetter(key):
            self.pendu.draw()
        self.clavier.desactivate(key)
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
