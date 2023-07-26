"""
Création d'une classe Config permettant de créer un objet de configuration
à partir d'un fichier JSON et de sauvegarder les modifications apportées
"""

import json


class Config:
    def __init__(self, json_file: str) -> None:
        with open(json_file) as file:
            json_data = json.load(file)
        self.json_data = json_data

    def toDict(self) -> dict:
        "Convertit l'objet en dictionnaire"
        return self.json_data

    def listContent(self) -> None:
        print('Voici le contenu de la configuration')
        print(self.json_data)

    def toJSON(self):
        # La méthode magique __dict__ transforme l'objet en dictionnaire (?)
        return json.dumps(self.__dict__)


def main():
    """
    Tests sur la classe Config
    """
    json_file = "./data/conf.json"
    configObject = Config(json_file)    # Création d'un objet
    config = configObject.toDict()      # Conversion en dictionnaire
    configObject.listContent()
    print(config['canevas'])
    print(config['letters']['active'])


if __name__ == "__main__":
    main()
