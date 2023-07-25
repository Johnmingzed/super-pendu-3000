from tkinter import *


class Pendu(object):
    def __init__(self, canva: Canvas):
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
        self.color = '#FFA200'
        self.width = 5
        self.complete = False
        self.canva = canva
        self.canva.configure(width=400, height=400)

    def draw(self) -> bool:
        step = self.cursor
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


def main():
    root = Tk()
    root.title("Super Pendu 3000")

    canva = Canvas(root, background='#112233', height=400, width=400)
    canva.pack(side=TOP)

    pendu = Pendu(canva)

    def play():
        complete = pendu.draw()
        print(complete)
        pendu_state = "Rejouer" if complete else "Jouer"
        playButton.configure(text=pendu_state)

    playButton = Button(root, text="Jouer", command=play)
    playButton.pack(side=BOTTOM)

    root.mainloop()


if __name__ == "__main__":
    main()
