# Nom du fichier : main.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html

# Point d'entrée du programme


import List
import Theme
import random
from Word import Word
from Config import Config
from Pendu import Pendu
from DisplayWord import DisplayWord
from Keyboard import Keyboard
from ActionBar import ActionBar
from tkinter import *
from tkinter import messagebox
from WordMenu import WordMenu
import pygame
import string


class Main():

    def __init__(self) -> None:

        # Chargement de PyGame pour le son
        pygame.mixer.init()

        # Définition des sons
        self.victory_sound = "./app/src/sound-win.ogg"
        self.defeat_sound = "./app/src/sound-loose.ogg"

        # Chemin vers les fichiers de configuration
        self.xml_file = "./data/menus.xml"
        self.json_file = "./data/conf.json"
        self.sql_file = "./data/data.sq3"

        # Chargement du fichier de configuration
        self.config = Config(self.json_file).toDict()

        # Palette de couleurs
        if hasattr(self, "config"):
            bg_color = self.config['canevas']
        else:
            bg_color = '#112233'
            self.config = None

        # Fenêtre principale
        self.window = Tk()
        self.window.title("Super Pendu 3000")
        self.window.configure(background=bg_color)
        self.window.iconbitmap("./app/src/favicon.ico")
        self.window.minsize(1010,400)

        # Création du layout général
        self.layout = Canvas(
            self.window, background=bg_color, highlightthickness=0)
        self.layout.pack(expand=True, fill=BOTH)

        # Création du layout pendu
        self.area_pendu = Canvas(
            self.layout, background=bg_color, highlightthickness=0)
        self.area_pendu.pack(side=LEFT, expand=True, fill=BOTH)

        # Création du layout clavier + mot
        if self.config:
            bg_color2 = 'white'
        else:
            bg_color2 = bg_color
        self.area_info = Canvas(
            self.layout, background=bg_color2, highlightthickness=0)
        self.area_info.pack(side=RIGHT, expand=True, fill=BOTH)

        # Création du layout du mot
        self.area_word = Canvas(self.area_info, background=bg_color2,
                                highlightthickness=0)
        self.area_word.pack(expand=1)

        # Création du layout du clavier
        self.area_keyboard = Canvas(
            self.area_info, background=bg_color2, highlightthickness=0)
        self.area_keyboard.pack(expand=1)

        # Création des Mots
        self.wordlist = Word(self.sql_file)

        # Lancement de la partie
        self.newgame()


    def newgame(self, word: str = None) -> None:
        print("Initialisation d'une nouvelle partie")

        # Définition du mot à trouver
        if word:
            print('Nouveau mot fournit')
            self.word_to_guess = word
        else:
            print('Remise à zero de la liste des mots')
            self.wordlist.selectAll()
            self.wordlist.viewList()
            self.word_to_guess = self.wordlist.random()

        print(self.word_to_guess)

        # Création de la barre de menus
        menu = ActionBar(self.window, self.xml_file, self)

        # Instanciation de l'objet Pendu
        self.pendu = Pendu(self.area_pendu, self.config)

        # Instanciation de l'objet Keyboard
        self.clavier = Keyboard(self.area_keyboard, self.config,
                                column=10, alphabet="abcdefghijklmnopqrstuvwxyz")

        # Instanciation du l'objet Displayword avec trnasmission du mot
        self.display = DisplayWord(
            self.area_word, self.word_to_guess, self.config)

        # Suivi des tentatives
        self.letters_played = []

        # Tentative du joueur
        self.window.bind('<Key>', self.keyPlay)
        self.window.bind('<Button>', self.mousePlay)

        # Rendu de l'application
        self.window.mainloop()

    def keyPlay(self, e: Event) -> None:
        if not self.pendu.complete and not self.display.victory and e.char:
            # On vérifie que la touche entrée correspont à un caractère
            key = e.char
            if key in string.ascii_letters:
                self.play(key)

    def mousePlay(self, e: Event) -> None:
        if not self.pendu.complete and not self.display.victory:
            target_id = self.area_keyboard.find_closest(e.x, e.y)
            target_tags = self.area_keyboard.gettags(target_id)
            if len(target_tags) == 2:
                if target_tags[1] == 'current':
                    letter = target_tags[0]
                    self.play(letter)

    def play(self, key: str) -> None:
        if self.noRepeat(key):
            if not self.display.testLetter(key):
                self.pendu.draw()
            self.clavier.desactivate(key)
            self.display.display()
            self.victory()
            self.gameover()

    def playSound(self, file: str):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops=0)

    def gameover(self) -> None:
        if self.pendu.complete:
            self.playSound(self.defeat_sound)
            self.pendu.defeat()
            message = f"Désolé, mais vous avez perdu... Le mot était \"{self.word_to_guess}\".\nVoulez-vous faire une nouvelle partie ?"
            newgame = messagebox.askyesno("Game over", message)
            if newgame:
                self.newgame()
            return 1
        else:
            return 0

    def victory(self) -> None:
        if self.display.victory:
            self.playSound(self.victory_sound)
            self.pendu.victory()
            message = f"Vous avez trouvé le mot \"{self.word_to_guess}\" en {len(self.letters_played)} tentatives.\nVoulez-vous continuer ?"
            newgame = messagebox.askyesno("Victoire !", message)
            if newgame:
                self.newgame(self.wordlist.random())

    def noRepeat(self, key: str) -> bool:
        "Vérification que la lettre n'a pas déjà été jouée"
        if key in self.letters_played:
            print("Lettre déjà jouée")
            return 0
        else:
            self.letters_played.append(key)
            print("Lettres jouées :", self.letters_played)
            return 1

    def about(self) -> None:
        "Affichage de la boîte de dialogue 'À propos'"
        messagebox.showinfo(
            "À propos", "Bienvenue dans le jeu du pendu, il est sous licence GNU-GPL 3.0")

    def close(self) -> None:
        "Quitter l'application"
        self.window.destroy()

    def editWords(self) -> None:
        "Editer la liste des mots disponibles"
        self.word_edit = WordMenu(self.sql_file)
        x, y = self.window.winfo_x(), self.window.winfo_y()
        self.word_edit.word_menu.geometry(f"+{x+400}+{y+40}")
        print(self.window.winfo_height(), self.window.winfo_width())


if __name__ == "__main__":
    main = Main()
