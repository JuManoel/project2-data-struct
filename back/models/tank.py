import json

class Tank:
    def __init__(self, capacidad: float):
        self.capacidad = capacidad

    @classmethod
    def fromDict(cls, data: dict):
        return cls(capacidad=data.get('capacidad', 0.0))

    def toDict(self):
        return {'capacidad': self.capacidad}

    @classmethod
    def fromJson(cls, json_str: str):
        data = json.loads(json_str)
        return cls.fromDict(data)

    def toJson(self):
        return json.dumps(self.toDict())