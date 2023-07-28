# Nom du fichier : Pydo.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html


import sqlite3 as sqlite
from unidecode import unidecode



class Pydo(object):
    "Définition d'un objet Pydo permettant les actions de CRUD sur une basse de données SQLite3"

    def __init__(self, path: str, table: str) -> None:
        themes = ['themes', 'theme']
        mots = ['mots', 'mot']

        self.database = sqlite.connect(path)
        self.cur = self.database.cursor()
        if table == 'themes':
            self.table = themes
        elif table == 'mots':
            self.table = mots
        else:
            print("Aucune table correspondante dans la base de données")
            exit()

    def create(self, name: str) -> None:
        if name != "":
            name = self.formatText(name)
            sql = (name.lower(),)
            try:
                self.cur.execute(
                    f"INSERT INTO {self.table[0]}({self.table[1]}) VALUES(?)", sql
                )
                self.database.commit()
                print(f'---> "{name}" a bien été ajouté.')
            except sqlite.Error as e:
                print('---> Erreur lors de la création :', e)
        else:
            print("Vous ne pouvez pas enregistrer un chaîne vide.")

    def selectByName(self, name: str) -> tuple:
        name = self.formatText(name)
        sql = (name.lower(),)
        try:
            req = self.cur.execute(
                f"SELECT * FROM {self.table[0]} WHERE {self.table[1]}=?", sql
            )
            result = req.fetchone()
            if result:
                return result
            else:
                print(f"---> \"{sql}\" n'existe pas.")
        except sqlite.Error as e:
            print('---> Erreur lors de la séléction :', e)

    def selectAll(self) -> list:
        try:
            req = self.cur.execute(f"SELECT * FROM {self.table[0]}")
            return req.fetchall()
        except sqlite.Error as e:
            print('---> Erreur lors de la séléction :', e)

    def update(self, name: str, data: str) -> None:
        if self.selectByName(name):
            data = self.formatText(data)
            try:
                sql = (data, name)
                self.cur.execute(
                    f"UPDATE {self.table[0]} SET {self.table[1]}=? WHERE {self.table[1]}=?", sql)
                self.database.commit()
                print(f'---> Modification de {name} effectuée')
            except sqlite.Error as e:
                print('---> Erreur lors de la mise à jour', e)

    def delete(self, name: str):
        name = self.formatText(name)
        if self.selectByName(name):
            sql = (name,)
            try:
                self.cur.execute(
                    f"DELETE FROM {self.table[0]} WHERE {self.table[1]}=?", sql)
                self.database.commit()
                print(f'---> Le mot "{name}" effacé')
            except sqlite.Error as e:
                print('---> Erreur lors de la suppression :', e)

    def formatText(self, text: str) -> str:
        if len(text) > 0:
            unaccented_string = unidecode(text)
        return unaccented_string


if __name__ == "__main__":
    import os

    main_dir = os.path.split(os.path.abspath(__file__))[0]

    # Selection de la base de données
    path = os.path.join(main_dir, "data.sq3")

    # Instanciation d'une BDD
    bdd = Pydo(path, 'mots')

    test = bdd.selectAll()
    print(test, type(test))

    # update(45, 24)
    bdd.delete('JavaScript')
    bdd.create("Serveur")
    bdd.create("JavaScript")
    bdd.create("Front-end")
    bdd.create("Back-end")
    bdd.create("Full Stack")
    testOne = bdd.selectByName('Javascript')
    print(testOne)
    bdd.update('base de données', 'base de donnees')
    test = bdd.formatText('aàâäéèêëiÎoôöùüû')
    print(test)

    print('Programme terminé')
    # database.close()
