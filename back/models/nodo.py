import json
import json

class Nodo:
    def __init__(self, id: str, costo: float, tank=None):
        self.id = id
        self.costo = costo
        self.tank = tank
    def fromDict(self, data: dict):
        self.id = data.get('id', '')
        self.costo = data.get('costo', 0.0)
        self.tank = data.get('tank', None)

    def toDict(self) -> dict:
        return {
            'id': self.id,
            'costo': self.costo,
            'tank': self.tank
        }

    @classmethod
    def fromJson(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

    def toJson(self) -> str:
        return json.dumps(self.toDict())