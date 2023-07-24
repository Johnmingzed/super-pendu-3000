import sqlite3 as pydo

# Selection de la base de données
database = pydo.connect('bd_test.sq3')
cur = database.cursor()


def create(age: int, nom: str, taille: float) -> None:
    sql = (age, nom, taille)
    try:
        cur.execute(
            "INSERT INTO membres(age,nom,taille) VALUES(?,?,?)", sql
        )
        database.commit()
        print(f'---> {nom} a bien été crée.')
    except pydo.Error as e:
        print('---> Erreur lors de la création :', e)


def selectByName(nom: str) -> tuple:
    sql = (nom,)
    try:
        req = cur.execute(
            "SELECT * FROM membres WHERE nom=?", sql
        )
        result = req.fetchone()
        if result:
            return result
        else:
            print(f"---> L'utilisateur {nom} n'existe pas.")
    except pydo.Error as e:
        print('---> Erreur lors de la séléction :', e)


def selectAll() -> list:
    try:
        req = cur.execute("SELECT * FROM membres")
        return req.fetchall()
    except pydo.Error as e:
        print('---> Erreur lors de la séléction :', e)


def update(user, data) -> None:
    if selectByName(user):
        try:
            sql = (data, user)
            cur.execute("UPDATE membres SET age=? WHERE nom=?", sql)
            database.commit()
            print(f'---> Modification de {user} effectuée')
        except pydo.Error as e:
            print('---> Erreur lors de la mise à jour', e)


def delete(user: str):
    if selectByName(user):
        sql = (user,)
        try:
            cur.execute("DELETE FROM membres WHERE nom=?", sql)
            database.commit()
            print(f'---> Utilisateur {user} effacé')
        except pydo.Error as e:
            print('---> Erreur lors de la suppression :', e)


if __name__ == "__main__":
    test = selectAll()
    print(test, type(test))
    selectByName('Dupont')
    update(45, 24)
    delete('Jonathan')
    create(32, "Jonathan", 1.74)
    testOne = selectByName('Paul')
    print(testOne)
    update('Paul', 40)

    print('Programme terminé')
    # database.close()
