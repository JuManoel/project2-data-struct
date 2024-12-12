from back.models.barrio import Barrio
from back.models.aristaBarrio import AristaBarrio
import json

class Red:
    def __init__(self):
        self.red = {}

    def agregarBarrio(self, barrioId):
        if barrioId not in self.red:
            self.red[barrioId] = []

    def agregarArista(self, barrioId, arista: AristaBarrio):
        if barrioId in self.red:
            self.red[barrioId].append(arista)
        else:
            self.red[barrioId] = [arista]

    def obtenerAristas(self, barrio):
        return self.red.get(barrio, [])

    def __repr__(self):
        return f'Red({self.red})'

    def toJson(self):
        return json.dumps(self.toDict())

    @classmethod
    def fromJson(self, json_str):
        data = json.loads(json_str)
        self.fromDict(data)

    def toDict(self):
        return {
            'barrios': {barrio: [arista.toDict() for arista in aristas] for barrio, aristas in self.red.items()}
        }

    @classmethod
    def fromDict(self, data):
        self.red = {}
        for barrio, aristas in data['barrios'].items():
            self.red[barrio] = [AristaBarrio.fromDict(arista) for arista in aristas]

    def optimizarRed(self):
        pass