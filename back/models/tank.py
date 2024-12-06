import json

class Tank:
    def __init__(self, capacidad: float, capacidadTotal: float):
        self.capacidad = capacidad
        self.capacidadTotal = capacidadTotal

    @classmethod
    def fromDict(cls, data: dict):
        return cls(capacidad=data.get('capacidad', 0.0), capacidadTotal=data.get('capacidadTotal', 0.0))

    def toDict(self):
        return {'capacidad': self.capacidad,
                'capacidadTotal': self.capacidadTotal}


    @classmethod
    def fromJson(cls, json_str: str):
        data = json.loads(json_str)
        return cls.fromDict(data)

    def toJson(self):
        return json.dumps(self.toDict())