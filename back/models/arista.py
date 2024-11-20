from back.models.nodo import Nodo
import json
class Arista:
    def __init__(self, flujo: float, nodo: Nodo, obstruido: int, flujoOptimo: float):
        if obstruido not in [0, 1, 2]:
            raise ValueError("El valor de obstruido debe ser 0, 1 o 2")
        self.flujo = flujo
        self.nodo = nodo
        self.obstruido = obstruido
        self.flujoOptimo = flujoOptimo

    def __repr__(self):
        return f"Arista(flujo={self.flujo}, nodo={self.nodo}, obstruido={self.obstruido}, flujoOptimo={self.flujoOptimo})"
    @classmethod
    def fromDict(cls, data: dict):
        nodo = Nodo.fromDict(data['nodo'])
        return cls(data['flujo'], nodo, data['obstruido'], data['flujoOptimo'])

    def toDict(self) -> dict:
        return {
            'flujo': self.flujo,
            'nodo': self.nodo.toDict(),
            'obstruido': self.obstruido,
            'flujoOptimo': self.flujoOptimo
        }

    @classmethod
    def fromJson(cls, json_str: str):
        data = json.loads(json_str)
        return cls.fromDict(data)

    def toJson(self) -> str:
        return json.dumps(self.toDict())