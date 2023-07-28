# Nom du fichier : Pendu.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html

# Good icons created by Freepik - Flaticon
# https://www.flaticon.com/free-icons/good

# Bad icons created by Freepik - Flaticon
# https://www.flaticon.com/free-icons/bad

from tkinter import *
import os


class Pendu(object):
    "Définition d'un objet graphique pendu"

    def __init__(self, canva: Canvas, config: dict = None) -> None:
        main_dir = os.path.split(os.path.abspath(__file__))[0]

        self.config = config
        self.canva = canva
        self.canva.configure(width=400, height=400)
        # Effacement du canva en cas de nouvelle partie
        self.canva.delete('all')
        self.pattern = [
            ('line', 20, 380, 380, 380),
            ('line', 120, 380, 120, 20),
            ('line', 120, 20, 300, 20),
            ('line', 120, 60, 160, 20),
            ('line', 250, 20, 250, 100),
            ('oval', 230, 100, 270, 140),
            ('line', 250, 140, 250, 240),
            ('line', 250, 240, 220, 320),
            ('line', 250, 240, 280, 320),
            ('line', 250, 160, 220, 220),
            ('line', 250, 160, 280, 220)
        ]
        self.cursor = 0
        self.img_victory = PhotoImage(
            file=os.path.join(main_dir, "src/positive-vote.png"))
        self.img_defeat = PhotoImage(
            file=os.path.join(main_dir, "src/negative-vote.png"))
        if self.config:
            self.color = self.config['line']['color']
            self.width = self.config['line']['width']
        else:
            self.color = '#FFA200'
            self.width = 5
        self.complete = False

    def draw(self) -> bool:
        step = self.cursor
        self.canva.delete('image')
        if step <= len(self.pattern) - 1:
            self.complete = False
            drawPendu = self.pattern[step]
            if drawPendu[0] == 'line':
                self.canva.create_line(drawPendu[1], drawPendu[2], drawPendu[3],
                                       drawPendu[4], fill=self.color, width=self.width)
            elif drawPendu[0] == 'oval':
                self.canva.create_oval(drawPendu[1], drawPendu[2], drawPendu[3],
                                       drawPendu[4], outline=self.color, width=self.width)
            self.cursor += 1
            if step == len(self.pattern) - 1:
                self.complete = True
        else:
            self.cursor = 0
            self.complete = False
            self.canva.delete('all')
        return self.complete

    def victory(self) -> None:
        self.cursor = 0
        self.canva.delete('all')
        self.canva.create_image(200, 200, image=self.img_victory, tags="image")

    def defeat(self) -> None:
        self.cursor = 0
        self.canva.delete('all')
        self.canva.create_image(200, 200, image=self.img_defeat, tags="image")


def main():
    root = Tk()
    root.title("Super Pendu 3000")

    canva = Canvas(root)
    canva.pack()

    pendu = Pendu(canva)

    def play():
        complete = pendu.draw()
        print(complete)
        pendu_state = "Rejouer" if complete else "Jouer"
        playButton.configure(text=pendu_state)

    playButton = Button(root, text="Jouer", command=play)
    playButton.pack(side=RIGHT)

    victoryButton = Button(root, text="Gagné", command=pendu.victory)
    victoryButton.pack(side=LEFT)

    victoryButton = Button(root, text="Perdu", command=pendu.defeat)
    victoryButton.pack(side=LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
