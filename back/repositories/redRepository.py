from back.models.red import Red
import json

class Repository:
    def __init__(self, filePath = "./red.json"):
        self.filePath = filePath

    def _readFile(self):
        try:
            with open(self.filePath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def _writeFile(self, data):
        with open(self.filePath, 'w') as file:
            json.dump(data, file, indent=4)

    def create(self, red: Red):
        self._writeFile(red.toDict())

    def read(self):
        data = self._readFile()
        if data:
            return Red.fromDict(data)
        return None

    def update(self, updatedRed: Red):
        self._writeFile(updatedRed.toDict())
        return True

    def delete(self):
        self._writeFile(None)
