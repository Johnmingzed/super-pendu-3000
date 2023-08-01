# Nom du fichier : AppearanceMenu.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html

# Classe d'objet représentant une fenêtre de gestion de l'apparence

from tkinter import *
from tkinter.colorchooser import askcolor
import json


class AppearanceMenu(object):
    "Classe représentant une fenêtre de gestion de l'apparence."

    def __init__(self, json_file: str, main_instance=None) -> None:
        # Ouverture du fichier JSON
        with open(json_file) as file:
            json_data = json.load(file)
        self.json_data = json_data
        self.main = main_instance
        self.json_file = json_file

        # Création de la fenêtre
        self.appearance_menu = Toplevel(padx=10, pady=10)
        self.appearance_menu.title(f"Édition de l'apparence du jeu")
        self.appearance_menu.resizable(0, 0)

        # Insertion du réglage pour le canevas
        ColorMenu(self.appearance_menu,"Canevas", "lemon chiffon", tag="canevas")

        # Insertion du réglage pour le background
        ColorMenu(self.appearance_menu, "Background", "white", tag="background")
        
        # Insertion du réglage pour les lettres actives
        ColorMenu(self.appearance_menu, "Lettres actives", "white", tag="background")

        # Insertion du réglage pour le canevas
        ColorMenu(self.appearance_menu, "Lettres utilisées", "grey", tag="letters active")

        # Insertion du réglage pour le canevas
        ColorMenu(self.appearance_menu, "Bordures et écritures", "black", tag="letters used")

        # Insertion du réglage pour le canevas
        ColorMenu(self.appearance_menu, "Couleur du pendu", "black", tag="line color")

        # Bouton Réinitialiser
        self.reset_button = Button(self.appearance_menu, text="Réinitialiser", command=None)
        self.reset_button.grid(row=ColorMenu.params, column=0, sticky=W, pady=(10,0))

        # Bouton Sauvegarder
        self.save_button = Button(self.appearance_menu, text="Sauvegarder", command=None)
        self.save_button.grid(row=ColorMenu.params, column=1, sticky=E, pady=(10,0))

class ColorMenu(object):
    "Classe représentant un label associé à un bouton dont on peut changer la couleur."

    params = 0

    def __init__(self, parent: AppearanceMenu, label: str, color: str, tag:str) -> None:
        self.parent = parent
        self.label = label
        self.color = color
        self.tag = tag
        self.createColorMenu()
        ColorMenu.params += 1

    def createColorMenu(self) -> None:
        # Création d'un label
        Label(self.parent, text=self.label).grid(
            row=ColorMenu.params, column=0, sticky=E, pady=2)

        # Création d'un bouton
        self.color_picker = Button(
            self.parent, text="", width=5, command=self.pickColor, background=self.color)
        self.color_picker.grid(row=ColorMenu.params, column=1, pady=2)

    def pickColor(self):
        "Ouverture d'une palette de couleur"
        color = askcolor(title="Couleur du canevas")
        self.color_picker.configure(background=color[1])

    def saveColor(self):
        "Sauvegarde des couleurs assignées à chaque item"


if __name__ == '__main__':
    import os
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    json_file = os.path.join(main_dir, "data/conf.json")

    root = Tk()
    root.title("Super AppearanceMenu 3000")

    appearance_menu = AppearanceMenu(json_file)

    root.mainloop()
