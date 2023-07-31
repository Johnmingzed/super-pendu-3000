# Nom du fichier : ActionBar.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html


import xml.etree.ElementTree as xml
from tkinter import *
from tkinter import messagebox


class ActionBar(object):
    "Définition d'un menu d'application"

    def __init__(self, window, xml_file, main_instance, wordlist=None) -> None:
        # Parse le fichier XML et obtient l'élément racine
        data = xml.parse(xml_file)
        menus = data.getroot()
        self.window = window
        self.main = main_instance
        # Création de la barre de menu
        self.action_bar = Menu(self.window)
        self.wordlist = wordlist
        # Etat du sous-menu thème en variable globale
        self.selected_theme = StringVar()

        # Création des menus principaux
        for submenu in menus:
            # On peut accéder aux attributs de chaque élément avec la syntaxe element.attrib
            # Par exemple, si l'élément a un attribut "id", on peut l'obtenir avec element.attrib["id"]
            menu = Menu(self.action_bar, tearoff=0)
            self.action_bar.add_cascade(
                label=submenu.attrib['categorie'], menu=menu)

            # Création des liens des menus
            # On peut accéder au noeud enfant par leur index
            for link in submenu:
                label = link.find("label").text
                command = link.find("command").text
                if command == 'choosetheme':
                    self.addOptions(menu, command, label)
                else:
                    menu.add_command(
                        label=label, command=self.create_command(command))

        # Affichage de la barre de menu
        self.window.config(menu=self.action_bar)

    def create_command(self, command_name: str):
        # Vérifier si la méthode associée à la commande existe dans la classe ActionBar
        if hasattr(self.main, command_name):
            return getattr(self.main, command_name)
        else:
            # Fonction de commande par défaut si la commande n'est pas définie
            return lambda: print(f"Commande '{command_name}' non définie.")

    def addOptions(self, menu: Menu, command: str, label: str) -> None:
        if command == 'choosetheme':
            theme_menu = Menu(menu, tearoff=0)
            menu.add_cascade(menu=theme_menu, label=label)
            themes_list = self.wordlist.availableThemes()

            for theme in themes_list:
                theme_menu.add_radiobutton(label=theme[1].capitalize(
                ), variable=self.selected_theme, value=theme, command=self.changeTheme)

    def changeTheme(self):
        theme_tuple = (int(self.selected_theme.get()[
                       :1]), self.selected_theme.get()[2:])
        self.main.setThemes(theme_tuple)


class Main():

    def __init__(self) -> None:

        main_dir = os.path.split(os.path.abspath(__file__))[0]

        # Chemin vers le fichier XML
        xml_file = os.path.join(main_dir, "./data/menus.xml")
        sql_file = os.path.join(main_dir, "data/data.sq3")

        # Fenêtre principale
        window = Tk()
        window.title("Super Pendu 3000")

        # Création des Mots à parti d'un thème
        wordlist = Word(sql_file, 'devops')

        # Création de la barre de menus
        menu = ActionBar(window, xml_file, self, wordlist)

        # Rendu de l'application
        window.mainloop()

    def about(self):
        print('A propos')

    def close(self):
        print('Fermeture')

    def newgame(self):
        print('Newgame')

    def choosetheme(self):
        print('Thematique')

    def setThemes(self, *args):
        print('Changement du thème par défaut')


if __name__ == "__main__":
    import os
    from Word import Word

    main = Main()
