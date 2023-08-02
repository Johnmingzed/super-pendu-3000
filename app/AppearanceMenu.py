# Nom du fichier : AppearanceMenu.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html

# Classe d'objet représentant une fenêtre de gestion de l'apparence

from tkinter import *
from tkinter.colorchooser import askcolor
from Config import Config
import json


class AppearanceMenu(object):
    "Classe représentant une fenêtre de gestion de l'apparence."

    def __init__(self, config: Config, main_instance=None) -> None:
        # Récupération de la configuration
        self.main = main_instance
        self.config_constructor = config
        self.config = self.config_constructor.toDict()

        # Création de la fenêtre
        self.appearance_menu = Toplevel(padx=10, pady=10)
        self.appearance_menu.title(f"Édition de l'apparence du jeu")
        self.appearance_menu.resizable(0, 0)
        self.appearance_menu.attributes("-topmost", "true")

        # Insertion du réglage pour le canevas
        ColorMenu(self, "Canevas", tag="canevas")

        # Insertion du réglage pour le background
        ColorMenu(self, "Background", tag="background")

        # Insertion du réglage pour les lettres actives
        ColorMenu(self, "Lettres actives", tag="letters active")

        # Insertion du réglage pour le canevas
        ColorMenu(self, "Lettres utilisées", tag="letters used")

        # Insertion du réglage pour le canevas
        ColorMenu(self, "Bordures et écritures", tag="letters border")

        # Insertion du réglage pour le canevas
        ColorMenu(self, "Couleur du pendu", tag="line color")

        # Message
        message = Label(self.appearance_menu, wraplength=180,
                        text="Les modifications seront appliquées après le redémarrage de l'application.")
        message.grid(row=(ColorMenu.instance_number+1), columnspan=2, pady=(10,0))
        ColorMenu.instance_number += 2

        # Bouton Réinitialiser
        self.reset_button = Button(
            self.appearance_menu, text="Réinitialiser", command=self.resetAll)
        self.reset_button.grid(row=ColorMenu.instance_number,
                               column=0, sticky=W, pady=(10, 0))

        # Bouton Sauvegarder
        self.save_button = Button(
            self.appearance_menu, text="Sauvegarder", command=self.save)
        self.save_button.grid(row=ColorMenu.instance_number,
                              column=1, sticky=E, pady=(10, 0))

    def resetAll(self):
        "Réinitialisation des couleurs par défaut et fermeture"
        self.config_constructor.resetColors()
        self.appearance_menu.destroy()

    def save(self):
        "Sauvegarde de la configuration et fermeture"
        ColorMenu.saveAll()
        self.appearance_menu.destroy()



class ColorMenu(object):
    "Classe représentant un label associé à un bouton dont on peut changer la couleur."

    instances = []
    instance_number = 0

    def __init__(self, parent: AppearanceMenu, label: str, tag: str) -> None:
        self.parent = parent
        self.label = label
        self.tag = tag
        self.config = parent.config
        self.color = self.colorByTag()
        self.createColorMenu()
        ColorMenu.instance_number += 1
        ColorMenu.instances.append(self)

    def colorByTag(self) -> str:
        self.subDict = self.tag.split()
        if len(self.subDict) > 1:
            color = self.config[self.subDict[0]][self.subDict[1]]
        else:
            color = self.config[self.subDict[0]]
        return color

    def createColorMenu(self) -> None:
        # Création d'un label
        Label(self.parent.appearance_menu, text=self.label).grid(
            row=ColorMenu.instance_number, column=0, sticky=E, pady=2)

        # Création d'un bouton
        self.color_picker = Button(
            self.parent.appearance_menu, text="", width=5, command=self.pickColor, background=self.color)
        self.color_picker.grid(row=ColorMenu.instance_number, column=1, pady=2)

    def pickColor(self):
        "Ouverture d'une palette de couleur"
        self.picked_color = askcolor(title="Couleur du canevas")
        self.color_picker.configure(background=self.picked_color[1])

    def saveColor(self):
        "Sauvegarde des couleurs assignées à chaque item"
        if hasattr(self, "picked_color"):
            config = self.parent.config_constructor
            key = self.subDict
            value = self.picked_color[1]
            config.saveColor((key, value))

    @classmethod
    def saveAll(cls):
        for instance in cls.instances:
            instance.saveColor()


class Preview(object):
    "Représentation d'un apperçu graphique de la configuration (à développer)"

    # Classe à développer


if __name__ == '__main__':
    import os
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    json_file = os.path.join(main_dir, "data/test.json")

    root = Tk()
    root.title("Super AppearanceMenu 3000")

    config = Config(json_file, root)
    appearance_menu = AppearanceMenu(config)

    root.mainloop()
