from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.arista import Arista
from back.models.nodo import Nodo
import json
class AristaBarrio(Arista):
    def __init__(self, flujo: float, tankId: str, obstruido: int, barrioId: str, nodoId: str, flujoOptimo: float):
        self.tankId = tankId
        super().__init__(flujo, nodoId, obstruido, flujoOptimo)
        self.barrioId = barrioId
    def toDict(self):
        return {
            'flujo': self.flujo,
            'flujoOptimo': self.flujoOptimo,
            'tankId': self.tankId,
            'obstruido': self.obstruido,
            'barrioId': self.barrio,
            'nodoId': self.nodoId,
        }

    @classmethod
    def fromDict(cls, data):
        tank = Nodo.fromDict(data['tank'])
        barrio = Barrio.fromDict(data['barrio'])
        nodo = Nodo.fromDict(data['nodoIntermedio'])
        return cls(data['flujo'], data,tank, data['obstruido'], barrio, nodo, data['flujoOptimo'])

    def toJson(self):
        return json.dumps(self.toDict())

    @classmethod
    def fromJson(cls, json_str):
        data = json.loads(json_str)
        return cls.fromDict(data)
