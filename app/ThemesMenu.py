# Nom du fichier : ThemesMenu.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html

# Classe d'objet représentant une fenêtre de gestion des themes

from tkinter import *
from Pydo import Pydo
from WordMenu import WordMenu


class ThemesMenu(WordMenu):
    "Classe représentant une fenêtre de gestion des themes."

    def __init__(self, bdd: str):
        super().__init__(bdd, 'thèmes')
        self.words_to_assign = Pydo(bdd, 'mots')

        # Redimensionnement de la fenêtre
        self.word_menu.geometry("510x350")
        self.word_menu.configure()

        # Container de sélection des mots
        self.selection_layout = Frame(self.word_menu)
        self.selection_layout.pack(side=RIGHT, fill=Y, padx=(0, 10), pady=10)

        # Repositionnement du container de droite
        self.right_layout.pack_forget()
        self.right_layout.pack(expand=True, fill=Y)

        # Bouton de modification
        self.list_button = Button(
            self.selection_layout, text="Sauvegarder", state=DISABLED, command=None)
        self.list_button.pack(side=BOTTOM, fill=X, pady=(10, 0))

        # Liste des mots
        selection_scrollbar = Scrollbar(self.selection_layout)
        selection_scrollbar.pack(side=RIGHT, fill=Y)
        self.selection = Listbox(self.selection_layout, height=15, selectmode=MULTIPLE,
                                 yscrollcommand=selection_scrollbar.set)
        self.createSelection()  # Remplissage de la liste
        self.selection.pack(side=RIGHT, fill=Y)
        selection_scrollbar.config(command=self.selection.yview)
        self.selection.bind("<<ListboxSelect>>", self.createSelection)

    def createSelection(self):
        self.selection.delete(0, END)
        list = sorted(self.words_to_assign.selectAll(),
                      key=lambda word: word[1])
        for word in list:
            self.selection.insert(END, word[1])

    def clearSelection(self):
        self.selection.select_clear(0, END)
        self.selection.delete(0, END)
        self.list_button.configure(state=DISABLED)
        self.selection.configure(state=DISABLED)
        print('clearSelection()')

    def clearModif(self):
        self.modify_word.delete(0, END)
        self.liste.select_clear(0, END)
        self.modif_button.configure(state=DISABLED)
        self.delete_button.configure(state=DISABLED)
        self.modify_word.configure(state=DISABLED)
        self.word_to_modify = None
        self.clearSelection()
        print("ThemesMenu")


if __name__ == '__main__':
    import os
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    sql_file = os.path.join(main_dir, "data/data.sq3")

    root = Tk()
    root.title("Super ThemesMenu 3000")

    x, y = root.winfo_x(), root.winfo_y()

    themes_edit = ThemesMenu(sql_file)
    themes_edit.word_menu.geometry(f"+{x+400}+{y+40}")

    root.mainloop()
