# Nom du fichier : Keyboard.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html


from tkinter import *
import math


class Keyboard(object):
    "Défintion d'un objet graphique clavier"

    alphabet = "azertyuiopqsdfghjklmwxcvbn"
    color = '#FFA200'
    active_color = '#FFE0AA'
    used_color = 'red'
    line_width = 3
    offset = 10
    key_size = 50
    key_per_line = 10
    rows = 0
    keyboard_width = 800
    keyboard_height = 400

    def __init__(self, canva: Canvas,  config: dict = None, alphabet: str = alphabet, column: int = key_per_line) -> None:
        self.config = config
        if self.config:
            self.color = self.config['letters']['border']
            self.active_color = self.config['letters']['active']
            self.used_color = self.config['letters']['used']
        self.canva = canva
        # Effacement du canva en cas de nouvelle partie
        self.canva.delete('all')
        self.alphabet = alphabet
        self.key_per_line = column
        self.key_list = self.key_row()
        self.draw_keyboard()
        self.keyboard_height = self.key_size * \
            self.rows + (self.offset + 1) * self.rows
        self.keyboard_width = self.key_size * self.key_per_line + \
            (self.offset + 1) * self.key_per_line
        self.canva.configure(width=self.keyboard_width,
                            height=self.keyboard_height)

    def draw_key(self, x: int = offset, y: int = offset, width: int = key_size, height: int = key_size, letter: str = 'A'):
        "Dessine une touche de clavier"
        self.round_rectangle(x, y, x+width, y+height,
                            outline=self.color, fill=self.active_color, width=self.line_width, tags=letter)
        self.canva.create_text(x+width/2, y+height/2, text=letter.upper(), tags=letter,
                            fill=self.color, font=('Consolas bold', 20))

    def draw_key_line(self, word: str, line: int = 0):
        "Dessine une rangée de touche de clavier"
        position = 0
        for letter in word:
            self.draw_key(self.offset + (self.key_size+self.offset) * position,
                            self.offset + (self.key_size+self.offset) * line,
                            letter=letter)
            position += 1

    def draw_keyboard(self):
        line = 0
        for word in self.key_list:
            self.draw_key_line(word, line)
            line += 1

    def desactivate(self, key_id):
        # print('Lettre', key_id, 'cliquée')
        target = self.canva.find_withtag(key_id)[0]
        self.canva.itemconfig(target, fill=self.used_color,
                            outline=self.used_color)

    def key_row(self) -> list:
        "Répartis les lettres de l'alphabet sur plusieurs lignes"
        self.rows = math.ceil(len(self.alphabet) / self.key_per_line)
        line = 0
        start = 0
        end = self.key_per_line
        key_rows = []
        while line < self.rows:
            line += 1
            key_rows.append(self.alphabet[start:end])
            start, end = end, end + self.key_per_line
        return key_rows

    def round_rectangle(self, x1: int, y1: int, x2: int, y2: int, radius: int = 20, **kwargs):
        points = [x1+radius, y1,
                    x1+radius, y1,
                    x2-radius, y1,
                    x2-radius, y1,
                    x2, y1,
                    x2, y1+radius,
                    x2, y1+radius,
                    x2, y2-radius,
                    x2, y2-radius,
                    x2, y2,
                    x2-radius, y2,
                    x2-radius, y2,
                    x1+radius, y2,
                    x1+radius, y2,
                    x1, y2,
                    x1, y2-radius,
                    x1, y2-radius,
                    x1, y1+radius,
                    x1, y1+radius,
                    x1, y1]
        return self.canva.create_polygon(points, **kwargs, smooth=True)


def main():

    def mousePlay(e):
        target_id = canva.find_closest(e.x, e.y)
        target_tags = canva.gettags(target_id)
        if len(target_tags) == 2:
            if target_tags[1] == 'current':
                letter = target_tags[0]
                clavier.desactivate(letter)

    root = Tk()
    root.title("Super Clavier 3000")

    canva = Canvas(root)
    canva.pack()

    clavier = Keyboard(canva, column=10, alphabet='abcdefghijklmnopqrstuvwxyz')

    canva.bind('<Button>', mousePlay)

    root.mainloop()


if __name__ == "__main__":
    main()
