from tkinter import *
import math


class Keyboard(object):
    "Défintion d'un objet graphique clavier"

    alphabet = "azertyuiopqsdfghjklmwxcvbn"
    color = '#FFA200'
    offset = 10
    key_size = 50
    key_per_line = 10
    rows = 0
    keyboard_width = 800
    keyboard_height = 400

    def __init__(self, canva: Canvas, alphabet: str = alphabet, column: int = key_per_line) -> None:
        self.canva = canva
        self.alphabet = alphabet
        self.key_per_line = column
        self.key_list = self.key_row()
        self.draw_keyboard()
        self.keyboard_height = self.key_size * self.rows + (self.offset + 1) * self.rows
        self.keyboard_width = self.key_size * self.key_per_line + (self.offset + 1) * self.key_per_line
        self.canva.configure(width=self.keyboard_width, height=self.keyboard_height)

    def draw_key(self, x: int = offset, y: int = offset, width: int = key_size, height: int = key_size, letter: str = 'A'):
        "Dessine une touche de clavier"
        self.round_rectangle(x, y, x+width, y+height,
                             outline=self.color, fill='', width=3, tags=letter)
        self.canva.create_text(x+width/2, y+height/2, text=letter,
                               fill=self.color, font=('Arial 20 bold'))

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
    root = Tk()
    root.title("Super Clavier 3000")

    canva = Canvas(root)
    canva.pack()

    clavier = Keyboard(canva, column=10)

    root.mainloop()


if __name__ == "__main__":
    main()
