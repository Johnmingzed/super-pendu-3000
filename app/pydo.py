# Nom du fichier : Pydo.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html


import sqlite3 as sqlite
from unidecode import unidecode


class Pydo(object):
    "Définition d'un objet Pydo permettant les actions de CRUD sur une basse de données SQLite3"

    THEMES = ['themes', 'theme']
    MOTS = ['mots', 'mot']

    def __init__(self, path: str, table: str) -> None:
        # themes = ['themes', 'theme']
        # mots = ['mots', 'mot']

        self.database = sqlite.connect(path)
        self.cur = self.database.cursor()
        if table == 'themes':
            self.table = self.THEMES
        elif table == 'mots':
            self.table = self.MOTS
        else:
            print("Aucune table correspondante dans la base de données")
            exit()

    def define(self, table: str = None, column: str = None) -> tuple:
        if not table:
            table = self.table[0]
        if not column:
            column = self.table[1]
        return (table, column)

    def create(self, name: str, table: str = None, column: str = None) -> None:
        table, column = self.define(table, column)
        if name != "":
            name = self.formatText(name)
            sql = (name.lower(),)
            try:
                self.cur.execute(
                    f"INSERT INTO {table}({column}) VALUES(?)", sql
                )
                self.database.commit()
                print(f'---> "{name}" a bien été ajouté.')
            except sqlite.Error as e:
                print('---> Erreur lors de la création :', e)
        else:
            print("Vous ne pouvez pas enregistrer un chaîne vide.")

    def selectByName(self, name: str, table: str = None, column: str = None) -> tuple:
        table, column = self.define(table, column)
        name = self.formatText(name)
        sql = (name.lower(),)
        try:
            req = self.cur.execute(
                f"SELECT * FROM {table} WHERE {column}=?", sql
            )
            result = req.fetchone()
            if result:
                return result
            else:
                print(f"---> \"{sql}\" n'existe pas.")
        except sqlite.Error as e:
            print('---> Erreur lors de la séléction :', e)

    def selectAll(self, table: str = None, column: str = None) -> list:
        table, column = self.define(table, column)
        try:
            req = self.cur.execute(f"SELECT * FROM {table}")
            return req.fetchall()
        except sqlite.Error as e:
            print('---> Erreur lors de la séléction :', e)

    def update(self, name: str, data: str, table: str = None, column: str = None) -> None:
        table, column = self.define(table, column)
        if self.selectByName(name):
            data = self.formatText(data)
            try:
                sql = (data, name)
                self.cur.execute(
                    f"UPDATE {table} SET {column}=? WHERE {column}=?", sql)
                self.database.commit()
                print(f'---> Modification de {name} effectuée')
            except sqlite.Error as e:
                print('---> Erreur lors de la mise à jour', e)

    def delete(self, name: str, table: str = None, column: str = None):
        table, column = self.define(table, column)
        name = self.formatText(name)
        if self.selectByName(name):
            sql = (name,)
            try:
                self.cur.execute(
                    f"DELETE FROM {table} WHERE {column}=?", sql)
                self.database.commit()
                print(f'---> Le mot "{name}" effacé')
            except sqlite.Error as e:
                print('---> Erreur lors de la suppression :', e)

    def formatText(self, text: str) -> str:
        if len(text) > 0:
            unaccented_string = unidecode(text)
        return unaccented_string

    def saveList(self, theme: str, words: list = None) -> None:
        # On reparts d'une liste vierge dont on récupère l'ID
        id_theme = self.cleanList(theme)
        print(id_theme)
        # On récupère les ID correspondantes au mot de la liste fournie
        words_list = words
        if words_list:
            for word in words_list:
                id_mot = self.selectByName(word, self.MOTS[0], self.MOTS[1])
                # On les enregistre dans la table mots_themes en les associations à l'ID du thème
                sql = (id_theme[0], id_mot[0])
                try:
                    self.cur.execute(
                        f"INSERT INTO 'mots_themes' ('id_themes', 'id_mots') VALUES(?,?)", sql
                    )
                    self.database.commit()
                    print(f"---> L'association {id_theme[1]}[{id_mot[1]}] a bien été ajouté.")
                except sqlite.Error as e:
                    print('---> Erreur lors de la création :', e)

    def cleanList(self, theme: str) -> int:
        table = self.THEMES[0]
        column = self.THEMES[1]
        id_theme = self.selectByName(theme, table, column)
        sql = (id_theme[0],)

        try:
            self.cur.execute(
                f"DELETE FROM mots_themes WHERE id_themes=?", sql
            )
            self.database.commit()
            print(f"Associations avec {theme} nettoyées")
        except sqlite.Error as e:
            print('---> Erreur lors de la suppression :', e)

        return (id_theme)


if __name__ == "__main__":
    import os

    main_dir = os.path.split(os.path.abspath(__file__))[0]

    # Selection de la base de données
    path = os.path.join(main_dir, "data/data.sq3")

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
    bdd.saveList('chats', ['python', 'scrum', 'apache'])

    print('Programme terminé')
    # database.close()
