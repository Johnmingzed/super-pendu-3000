# Nom du fichier : WordMenu.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html

# Classe d'objet représentant une fenêtre de gestion des mots

from tkinter import *
from Pydo import Pydo
from unidecode import unidecode


class WordMenu(object):
    "Classe représentant une fenêtre de gestion des mots."

    def __init__(self, bdd: str, table: str = "mots") -> None:
        # Appel de la BDD
        self.table = table
        bdd_table = unidecode(table)
        self.words = Pydo(bdd, bdd_table)

        # Création de la fenêtre
        self.word_menu = Toplevel()
        self.word_menu.title(f"Édition des {self.table} à utiliser")
        self.word_menu.geometry("350x350")
        self.word_menu.resizable(0, 1)
        self.word_menu.minsize(350, 250)

        # Container pour la liste
        self.list_layout = Frame(self.word_menu)
        self.list_layout.pack(side=LEFT, fill=Y, padx=10, pady=10)

        # Container de droite
        self.right_layout = Frame(self.word_menu)
        self.right_layout.pack(side=RIGHT, fill=BOTH, expand=True)

        # Container pour les actions
        self.actions_layout = Frame(self.right_layout)
        self.actions_layout.pack(
            side=BOTTOM, fill=BOTH, expand=True, padx=(0, 10), pady=(0, 10))
        self.actions_layout.grid_columnconfigure(0, weight=1)
        self.actions_layout.grid_columnconfigure(1, weight=1)
        self.actions_layout.grid_rowconfigure(0, weight=0)
        self.actions_layout.grid_rowconfigure(1, weight=0)

        # Container pour les infos
        self.infos_layout = Frame(self.right_layout)
        self.infos_layout.pack(side=TOP, fill=X)

        # Texte d'information
        infos = f"Vous pouvez directement ajouter un nouveau {self.table[:-1]} dans le champ ci-contre (les accents seront automatiquement retirés) ou sélectionner un {self.table[:-1]} dans la liste pour le modifier ou le supprimer."
        self.info = Label(self.infos_layout, text=infos, font=("Arial", 10))
        self.info.bind("<Configure>", lambda e: self.info.config(
            wraplength=self.info.winfo_width()))
        self.info.pack(side=TOP, fill=X, padx=(0, 10), pady=10)

        # Bouton de modification
        self.modif_button = Button(
            self.actions_layout, text="Modifier", state=DISABLED, command=self.modify)
        self.modif_button.grid(row=1, column=0, sticky=N, pady=10)

        # Bouton de suppression
        self.delete_button = Button(
            self.actions_layout, text="Supprimer", state=DISABLED, command=self.delete)
        self.delete_button.grid(row=1, column=1, sticky=N, pady=10)

        # Création d'un champ de modification
        self.modify_word = Entry(self.actions_layout)
        self.modify_word.configure(state=DISABLED)
        self.modify_word.bind("<Return>", self.modify)
        self.modify_word.grid(row=0, columnspan=2, sticky=EW, pady=10)

        # Création d'un champ de saisie
        self.enter_word = Entry(self.list_layout)
        self.enter_word.insert(0, f"Ajouter un {self.table[:-1]}")
        self.enter_word.configure(state=DISABLED)
        self.enter_word.bind("<Button>", self.enterText)
        self.enter_word.bind("<Return>", self.validText)
        self.enter_word.bind("<FocusOut>", self.leaveText)
        self.enter_word.pack(side=TOP, fill=X, pady=(0, 10))

        # Création d'un scrollbar
        scrollbar = Scrollbar(self.list_layout)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Création de la liste des mots
        self.liste = Listbox(self.list_layout, height=15,
                             yscrollcommand=scrollbar.set)
        self.createList()  # Remplissage de la liste
        self.liste.pack(side=LEFT, fill=Y)
        scrollbar.config(command=self.liste.yview)
        self.liste.bind("<<ListboxSelect>>", self.displayWord)

    def displayWord(self, event=None):
        selection = self.liste.curselection()
        if selection:
            word = self.liste.get(selection[0])
            self.activeModify(word)

    def activeModify(self, word):
        self.word_to_modify = word
        self.modify_word.configure(state=NORMAL)
        self.modif_button.configure(state=NORMAL)
        self.delete_button.configure(state=NORMAL)
        self.modify_word.delete(0, END)
        self.modify_word.insert(0, word)

    def createList(self):
        self.liste.delete(0, END)
        list = sorted(self.words.selectAll(), key=lambda word: word[1])
        for word in list:
            self.liste.insert(END, word[1])

    def enterText(self, event):
        self.enter_word.configure(state=NORMAL)
        self.enter_word.delete(0, END)
        self.clearModif()

    def clearModif(self):
        self.modify_word.delete(0, END)
        self.liste.select_clear(0, END)
        self.modif_button.configure(state=DISABLED)
        self.delete_button.configure(state=DISABLED)
        self.modify_word.configure(state=DISABLED)
        self.word_to_modify = None

    def leaveText(self, event):
        self.enter_word.delete(0, END)
        self.enter_word.insert(0, f"Ajouter un {self.table[:-1]}")
        self.enter_word.configure(state=DISABLED)

    def validText(self, event):
        new_word = self.enter_word.get()
        self.words.create(new_word)
        self.enter_word.delete(0, END)
        self.createList()

    def modify(self, event=None):
        word = self.modify_word.get()
        self.words.update(self.word_to_modify, word)
        self.clearModif()
        self.createList()

    def delete(self):
        word = self.modify_word.get()
        self.words.delete(word)
        self.clearModif()
        self.createList()


if __name__ == '__main__':
    import os
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    sql_file = os.path.join(main_dir, "data/data.sq3")

    root = Tk()
    root.title("Super WordMenu 3000")

    word_menu = WordMenu(sql_file)

    root.mainloop()
