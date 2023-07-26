from tkinter import *
import tkinter.font as myfont


class DisplayWord(object):
    "Définition de l'affichage d'un mot à deviner"

    color = '#FFA200'
    offset = 5
    size = 40
    word_width = 600
    word_height = 200

    def __init__(self, canva: Canvas, baseword: str, config: dict = None) -> None:
        # Variable d'initialisation
        self.config = config
        if self.config:
            self.color = self.color = self.config['line']['color']
        self.victory = False
        self.score = 0
        self.canva = canva
        self.baseword = baseword
        self.lenght = len(baseword)
        self.rest = len(baseword)
        self.placeholder = ""
        self.custom_font = myfont.Font(
            family="Consolas", size=40, weight='bold')
        self.word_height = self.size + self.offset * 3
        self.word_width = self.size * self.lenght + \
            (self.lenght + 1) * self.offset

        # Méthode d'initialisation
        self.setPlaceHolder()
        self.canva.configure(width=self.word_width, height=self.word_height)
        self.display()

    def draw_letter(self, x: int = offset, y: int = offset, width: int = size, height: int = size, letter: str = 'A'):
        "Dessine une lettre du mot à trouver"
        self.canva.create_rectangle(x, y, x+width, y+height, fill='', width=0)
        self.canva.create_text(x+width/2, y+height/2, text=letter.upper(),
                               fill=self.color, font=self.custom_font)

    def display(self):
        "Dessine le mot à deviner"
        self.canva.delete('all')
        position = 0
        for letter in self.placeholder:
            self.draw_letter(self.offset + (self.size+self.offset) * position,
                             self.offset, letter=letter)
            position += 1

    def setPlaceHolder(self):
        for letter in self.baseword:
            self.placeholder += "_"

    def testLetter(self, letter_to_test: str) -> int:
        index = 0
        placeholder = self.placeholder
        newplaceholder = ""

        for letter in self.baseword:
            if letter == letter_to_test:
                newplaceholder += letter_to_test
            else:
                newplaceholder += placeholder[index]
            index += 1
        points = self.baseword.count(letter_to_test)
        isOK = self.winPoint(placeholder, newplaceholder, points)
        self.placeholder = newplaceholder
        return isOK

    def winPoint(self, old: str, new: str, point: int) -> int:
        if old != new:
            self.rest -= point
            self.score += 1
            if not self.rest:
                self.victory = True
                print('Vous avez gagné')
            return 1
        else:
            return 0


def main():

    def key_press(e):
        if not guess.victory:
            key = e.char
            guess.testLetter(key)
            guess.display()

    root = Tk()
    root.title("Super DisplayWord 3000")

    canva = Canvas(root)
    canva.pack()

    guess = DisplayWord(canva, 'developpeur')

    root.bind('<Key>', key_press)

    root.mainloop()


if __name__ == "__main__":
    main()
