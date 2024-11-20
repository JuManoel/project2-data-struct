from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.arista import Arista
from back.models.nodo import Nodo
import json
class AristaBarrio(Arista):
    def __init__(self, flujo: float, tank: Nodo, obstruido: int, barrio: Barrio, nodo: Nodo, flujoOptimo: float):
        if not tank.tank:
            raise ValueError("El nodo tiene tank tiene que tener un tank")
        super().__init__(flujo, tank, obstruido, flujoOptimo)
        self.barrio = barrio
        self.nodoIntermedio = nodo
    def toDict(self):
        return {
            'flujo': self.flujo,
            'flujoOptimo': self.flujoOptimo,
            'tank': self.tank.toDict(),
            'obstruido': self.obstruido,
            'barrio': self.barrio.toDict(),
            'nodoIntermedio': self.nodoIntermedio.toDict(),
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