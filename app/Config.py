# Nom du fichier : Config.py
# -*- coding: utf-8 -*-

# Ce code est sous licence GPL 3 (GNU General Public License version 3).
# Pour plus d'informations, consultez le fichier LICENSE ou visitez le site web :
# https://www.gnu.org/licenses/gpl-3.0.html


"""
Création d'une classe Config permettant de créer un objet de configuration
à partir d'un fichier JSON et de sauvegarder les modifications apportées
"""

import json


class Config:
    def __init__(self, json_file: str, main_instance=None) -> None:
        # Ouverture du fichier JSON
        with open(json_file) as file:
            json_data = json.load(file)
        self.json_data = json_data
        self.main = main_instance
        self.json_file = json_file

    def toDict(self) -> dict:
        "Convertit l'objet en dictionnaire"
        return self.json_data

    def listContent(self) -> None:
        "Affiche le contenu de l'objet"
        print('Voici le contenu de la configuration')
        print(self.json_data)

    def toJSON(self):
        "Convertit l'objet en JSON"
        # La méthode magique __dict__ transforme l'objet en dictionnaire (?)
        return json.dumps(self.__dict__)

    def save(self, to_save:tuple) -> None:
        "Modifie et sauvegarde l'objet"
        self.main.config.update(theme={'id':to_save[0], 'name':to_save[1]})
        save_json_data = json.dumps(self.main.config, indent=4)
        with open(self.json_file, "w") as file:
            file.write(save_json_data)
        print('💾 Configuration sauvegardée')



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
