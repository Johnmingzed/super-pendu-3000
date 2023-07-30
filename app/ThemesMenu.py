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
        self.radio_buttons = []
        self.scrollable_liste = Frame()
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
            self.selection_layout, text="Sauvegarder", state=DISABLED, command=self.saveSelection)
        self.list_button.pack(side=BOTTOM, fill=X, pady=(10, 0))

        # Liste des mots
        selection_scrollbar = Scrollbar(self.selection_layout)
        selection_scrollbar.pack(side=RIGHT, fill=Y)
        self.selection = Listbox(self.selection_layout, height=15, selectmode=MULTIPLE,
                                 yscrollcommand=selection_scrollbar.set)
        self.selection.pack(side=RIGHT, fill=Y)
        selection_scrollbar.config(command=self.selection.yview)

        # Remplacement de la liste de WordMenu par une Frame pour stocker les thêmes
        self.liste.destroy()
        self.scrollbar.destroy()

        self.liste = Canvas(self.list_layout)
        self.scrollbar = Scrollbar(
            self.list_layout, orient=VERTICAL, command=self.liste.yview)
        self.scrollable_liste = Frame(self.liste)
        self.scrollable_liste.bind("<Configure>", lambda e: self.liste.configure(
            scrollregion=self.liste.bbox("all")
        )
        )
        self.liste.create_window((0,0), window=self.scrollable_liste, anchor=NW)
        self.liste.configure(yscrollcommand=self.scrollbar.set)
        self.displayThemes()
        self.liste.pack(side=LEFT, fill=Y)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Stockage de l'index du thème sélectionné
        self.theme = None

        # Modification du message d'informations
        infos = f"Vous pouvez directement ajouter un nouveau {self.table[:-1]} dans le champ situé en haut à gauche (les accents seront automatiquement retirés).\n\nSélectionner un {self.table[:-1]} dans la liste de gauche pour le modifier ou le supprimer via les boutons ci-dessous ou éditer la liste de mots associés via la liste sur la droite."
        self.info.configure(text=infos)

    def displayThemes(self):
        self.clearThemes()
        self.var = StringVar()
        list = sorted(self.words.selectAll(), key=lambda word: word[1])
        for word in list:
            rb = Radiobutton(
                self.scrollable_liste, text=word[1], variable=self.var, value=word[1], command=self.selectTheme)
            rb.pack(anchor=W)
            self.radio_buttons.append(rb)
        self.var.set(None)
        self.liste.update_idletasks()
        self.liste.configure(width=self.scrollable_liste.winfo_reqwidth())

    def selectTheme(self, event=None):
        self.theme = self.var.get()
        self.createSelection()
        self.activeModify(self.theme)

    def createList(self):
        self.displayThemes()

    def clearThemes(self):
        if self.radio_buttons:
            for rb in self.radio_buttons:
                rb.destroy()
            self.radio_buttons = []

    def createSelection(self, event=None):
        self.selection.configure(state=NORMAL)
        self.selection.delete(0, END)
        list = sorted(self.words_to_assign.selectAll(),
                      key=lambda word: word[1])
        for word in list:
            self.selection.insert(END, word[1])
        self.list_button.configure(state=NORMAL)
        self.highlightSelection('mots')

    def highlightSelection(self, subject: str):
        higlight = self.words_to_assign.selectAllByAssociation(
            subject, self.theme)
        selection = self.selection.get(0, END)
        for word_in_selection in selection:
            word_to_verify = word_in_selection
            for word in higlight:
                if word_to_verify == word[1]:
                    index = selection.index(word_to_verify)
                    self.selection.select_set(index)

    def clearSelection(self):
        self.selection.select_clear(0, END)
        self.selection.delete(0, END)
        self.list_button.configure(state=DISABLED)
        self.selection.configure(state=DISABLED)
        self.theme = None

    def clearModif(self):
        self.modify_word.delete(0, END)
        self.modif_button.configure(state=DISABLED)
        self.delete_button.configure(state=DISABLED)
        self.modify_word.configure(state=DISABLED)
        self.word_to_modify = None
        self.clearSelection()
        self.displayThemes()

    def saveSelection(self, event=None):
        to_save = self.selection.curselection()
        words_to_save = []
        for i in to_save:
            words_to_save.append(self.selection.get(i))
        print(self.theme, "with", words_to_save)
        self.words_to_assign.saveList(self.theme, words_to_save)
        self.clearModif()


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
