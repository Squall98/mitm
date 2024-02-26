import os
from pathlib import Path
import json
import character.job as job

class Script():
    def __init__(self, character, script_path=None):
        self.character = character
        # Détermine le chemin du script JSON en utilisant le répertoire actuel du script
        if script_path is None:
            base_dir = Path(__file__).parent
            script_path = base_dir / "test.json"
        self.script_path = Path(script_path)
        self.script = self.load_script(self.script_path)

    def load_script(self, path):
        try:
            with path.open("r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement du script : {e}")
            return {}

    def action(self):
        map_id = self.character.map.mapID
        if map_id in self.script:
            action_type = self.script[map_id]
            self.perform_action(action_type)

    def perform_action(self, action_type):
        if action_type == "recolte":
            self.recolte_action()
        elif action_type == "combat":
            self.combat_action()

    def recolte_action(self):
        for cell in self.character.map.cells:
            if cell.isInteractive:
                job.recole(self.character, cell.CellID)

    def combat_action(self):
        print("Combat")

    def changer_map(self):
        pass  # Implémentation de changement de carte si nécessaire

# Point d'entrée si nécessaire
if __name__ == "__main__":
    pass  # Exemple d'utilisation
