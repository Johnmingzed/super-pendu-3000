# Nom du fichier : Config.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html


import json
import os


class Config:
    """
    Un objet Config permettant de stocker des donnéess de configuration
    à partir d'un fichier JSON.
    """

    def __init__(self, json_file: str, main_instance=None) -> None:
        """
        Initialise un objet Config à partir d'un fichier JSON.

        Args:
            json_file (str): Le chemin vers le fichier JSON de configuration.
            main_instance: L'instance principale à laquelle cette configuration est associée.
        """
        with open(json_file) as file:
            self.json_data = json.load(file)
        self.main = main_instance
        self.json_file = json_file

    def toDict(self) -> dict:
        """
        Convertit l'objet en dictionnaire.

        Returns:
            dict: Le dictionnaire représentant l'objet de configuration.
        """
        return self.json_data

    def listContent(self) -> None:
        """
        Affiche le contenu de l'objet.
        """
        print('Voici le contenu de la configuration :')
        print(self.json_data)

    def toJSON(self) -> str:
        """
        Convertit l'objet en JSON.

        Returns:
            str: L'objet converti en format JSON.
        """
        # La méthode magique __dict__ transforme l'objet en dictionnaire (?)
        return json.dumps(self.__dict__)

    def save(self, to_save: tuple) -> None:
        """
        Modifie et sauvegarde l'objet de configuration.

        Args:
            to_save (tuple): Un tuple contenant les données à sauvegarder.
        """
        self.main.config.update(theme={'id': to_save[0], 'name': to_save[1]})
        save_json_data = json.dumps(self.main.config, indent=4)
        with open(self.json_file, "w") as file:
            file.write(save_json_data)
        print('💾 Configuration sauvegardée')

    def saveColor(self, to_save: tuple) -> None:
        """
        Modifie et sauvegarde l'objet de configuration.

        Args:
            to_save (tuple): Un tuple contenant les données à sauvegarder.
        """
        print(f"{to_save[0]} : {to_save[1]}")
        if len(to_save[0]) == 1:
            self.json_data[to_save[0][0]] = to_save[1]
        else:
            self.json_data[to_save[0][0]][to_save[0][1]] = to_save[1]
        save_json_data = json.dumps(self.json_data, indent=4)
        with open(self.json_file, "w") as file:
            file.write(save_json_data)
        print('💾 Configuration sauvegardée')

    def resetColors(self) -> None:
        """
        Réinitialise les valeurs par défaut des couleurs.
        """
        default_colors = {'canevas': 'lemon chiffon', 'background': 'white', 'letters': {
            'active': 'white', 'used': 'grey', 'border': 'black'}, 'line': {'color': 'black', 'width': 5}, 'theme': {'id': 3, 'name': 'design'}}
        self.json_data.update(default_colors)
        save_json_data = json.dumps(self.json_data, indent=4)
        with open(self.json_file, "w") as file:
            file.write(save_json_data)
        print('💾 Configuration par défaut réinitialisée')

def main():
    """
    Tests sur la classe Config
    """
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    json_file = os.path.join(main_dir, "data/conf.json")
    configObject = Config(json_file)    # Création d'un objet
    config = configObject.toDict()      # Conversion en dictionnaire
    configObject.listContent()
    print(config['canevas'])
    print(config['letters']['active'])


if __name__ == "__main__":
    import os

    main()
