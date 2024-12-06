from back.models.barrio import Barrio
from back.models.aristaBarrio import AristaBarrio
import json

class Red:
    def __init__(self):
        self.barrios = {}

    def agregarBarrio(self, barrio):
        if barrio not in self.barrios:
            self.barrios[barrio] = []

    def agregarArista(self, barrio, arista):
        if barrio in self.barrios:
            self.barrios[barrio].append(arista)
        else:
            self.barrios[barrio] = [arista]

    def obtenerAristas(self, barrio):
        return self.barrios.get(barrio, [])

    def __repr__(self):
        return f'Red({self.barrios})'

    def toJson(self):
        return json.dumps(self.toDict())

    @classmethod
    def fromJson(self, json_str):
        data = json.loads(json_str)
        self.fromDict(data)

    def toDict(self):
        return {
            'barrios': {barrio: [arista.toDict() for arista in aristas] for barrio, aristas in self.barrios.items()}
        }

    @classmethod
    def fromDict(self, data):
        self.barrios = {}
        for barrio, aristas in data['barrios'].items():
            self.barrios[barrio] = [AristaBarrio.fromDict(arista) for arista in aristas]

    def optimizarRed(self):
        pass