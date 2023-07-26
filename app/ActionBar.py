import xml.etree.ElementTree as xml
from tkinter import *
from tkinter import messagebox


class ActionBar(object):
    "Définition d'un menu d'application"

    def __init__(self, window, xml_file, main_instance) -> None:
        # Parse le fichier XML et obtient l'élément racine
        data = xml.parse(xml_file)
        menus = data.getroot()
        self.window = window
        self.main = main_instance
        # Création de la barre de menu
        action_bar = Menu(self.window)

        # Création des menus principaux
        for submenu in menus:
            # On peut accéder aux attributs de chaque élément avec la syntaxe element.attrib
            # Par exemple, si l'élément a un attribut "id", on peut l'obtenir avec element.attrib["id"]
            menu = Menu(action_bar, tearoff=0)
            action_bar.add_cascade(
                label=submenu.attrib['categorie'], menu=menu)

            # Création des liens des menus
            # On peut accéder au noeud enfant par leur index
            for link in submenu:
                label = link.find("label").text
                command = link.find("command").text
                menu.add_command(
                    label=label, command=self.create_command(command))

        # Affichage de la barre de menu
        self.window.config(menu=action_bar)

    def create_command(self, command_name):
        # Vérifier si la méthode associée à la commande existe dans la classe ActionBar
        if hasattr(self, command_name):
            return getattr(self, command_name)
        else:
            # Fonction de commande par défaut si la commande n'est pas définie
            return lambda: print(f"Commande '{command_name}' non définie.")

#    def create_command(self, command_name):
#        # Recherche de la fonction de commande dans l'ensemble des namespaces
#        for namespace in [globals(), *globals().get("__builtins__", {})]:
#            command_function = namespace.get(command_name)
#            if callable(command_function):
#                return command_function

        # Fonction de commande par défaut si la commande n'est pas trouvée
        return lambda: print(f"Commande '{command_name}' non définie.")
        
        "Rechercher la function call"

    def about(self):
        "Affichage de la boîte de dialogue 'À propos'"
        self.main.about()

    def close(self):
        "Quitter l'application"
        # self.window.destroy()
        self.main.close()

    def newgame(self):
        "Lancer une nouvelle partie"
        self.main.newgame()

class Main():

    def __init__(self) -> None:

        # Chemin vers le fichier XML
        xml_file = "./data/menus.xml"

        # Fenêtre principale
        window = Tk()
        window.title("Super Pendu 3000")

        # Création de la barre de menus
        menu = ActionBar(window, xml_file, self)

        # Rendu de l'application
        window.mainloop()

    def about(self):
        print('A propos')

    def close(self):
        print('Fermeture')

    def newgame(self):
        print('Newgame')


if __name__ == "__main__":
    main = Main()
