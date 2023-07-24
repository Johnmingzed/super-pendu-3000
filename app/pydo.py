import sqlite3 as pydo

# Selection de la base de données
database = pydo.connect('./data/data.sq3')
cur = database.cursor()


def create(name: str) -> None:
    sql = (name.lower(),)
    if name != "":
        try:
            cur.execute(
                "INSERT INTO mots(mot) VALUES(?)", sql
            )
            database.commit()
            print(f'---> "{name}" a bien été ajouté.')
        except pydo.Error as e:
            print('---> Erreur lors de la création :', e)
    else:
        print("Vous ne pouvez pas enregistrer un chaîne vide.")


def selectByName(name: str) -> tuple:
    sql = (name.lower(),)
    try:
        req = cur.execute(
            "SELECT * FROM mots WHERE mot=?", sql
        )
        result = req.fetchone()
        if result:
            return result
        else:
            print(f"---> \"{name}\" n'existe pas.")
    except pydo.Error as e:
        print('---> Erreur lors de la séléction :', e)


def selectAll() -> list:
    try:
        req = cur.execute("SELECT * FROM mots")
        return req.fetchall()
    except pydo.Error as e:
        print('---> Erreur lors de la séléction :', e)


def update(name: str, data: str) -> None:
    if selectByName(name):
        try:
            sql = (data, name)
            cur.execute("UPDATE mots SET age=? WHERE mot=?", sql)
            database.commit()
            print(f'---> Modification de {name} effectuée')
        except pydo.Error as e:
            print('---> Erreur lors de la mise à jour', e)


def delete(name: str):
    if selectByName(name):
        sql = (name,)
        try:
            cur.execute("DELETE FROM mots WHERE mot=?", sql)
            database.commit()
            print(f'---> Le mot "{name}" effacé')
        except pydo.Error as e:
            print('---> Erreur lors de la suppression :', e)


if __name__ == "__main__":
    test = selectAll()
    print(test, type(test))

    # update(45, 24)
    delete('JavaScript')
    create("Serveur")
    create("JavaScript")
    create("Front-end")
    create("Back-end")
    create("Full Stack")
    testOne = selectByName('Javascript')
    print(testOne)
    # update('Paul', 40)

    print('Programme terminé')
    # database.close()
