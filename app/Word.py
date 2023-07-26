from Pydo import Pydo
import random

# Classe d'objet représentant un mot sauvegardé en BDD


class Word(Pydo):
    "Définition d'un objet contenant les mots"

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.pool = []
        self.selectAll()

    def selectAll(self) -> list:
        "Réinitialise la liste en récupérant tout les mots en base de données"
        self.pool.clear()
        for tuple in super().selectAll():
            self.pool.append(tuple[1])
        return self.pool

    def random(self) -> str:
        "Extrait un mot aléatoire de la liste"
        number = random.randrange(len(self.pool))
        picked = self.pool[number]
        self.pool.remove(picked)
        return picked

    def viewList(self) -> int:
        "Affiche le nombre d'élément restant dans la liste"
        print(self.pool,'\nReste :', len(self.pool))
        return len(self.pool)

if __name__ == "__main__":
    mot = Word("./data/data.sq3")

    mot.viewList()
    mot_random = mot.random()
    print(mot_random)
