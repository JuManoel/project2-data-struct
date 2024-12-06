import json

class Nodo:
    def __init__(self, id: str, tank=None):
        self.id = id
        self.tank = tank

    def __lt__(self, other):
        # Comparar nodos por sus IDs para heapq
        return self.id < other.id

    @classmethod
    def fromDict(self, data: dict):
        self.id = data.get('id', '')
        self.tank = data.get('tank', None)

    def toDict(self) -> dict:
        return {
            'id': self.id,
            'tank': self.tank.toDict() if self.tank else None
        }

    @classmethod
    def fromJson(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

    def toJson(self) -> str:
        return json.dumps(self.toDict())