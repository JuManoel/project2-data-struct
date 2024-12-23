from back.models.nodo import Nodo
import json
class Arista:
    def __init__(self, flujo: float, nodoId: str, obstruido: int, flujoOptimo: float):
        if obstruido not in [0, 1, 2]:
            raise ValueError("El valor de obstruido debe ser 0, 1 o 2")
        self.flujo = flujo
        self.nodoId = nodoId
        self.obstruido = obstruido
        self.flujoOptimo = flujoOptimo
        if obstruido == 1:
            self.flujo *= 10
        elif obstruido == 2:
            self.flujo = float('inf')

    def __repr__(self):
        return f"Arista(flujo={self.flujo}, nodo={self.nodoId}, obstruido={self.obstruido}, flujoOptimo={self.flujoOptimo})"
    @classmethod
    def fromDict(cls, data: dict):
        return cls(data['flujo'], data['nodoId'], data['obstruido'], data['flujoOptimo'])

    def toDict(self) -> dict:
        return {
            'flujo': self.flujo,
            'nodoId': self.nodoId,
            'obstruido': self.obstruido,
            'flujoOptimo': self.flujoOptimo
        }

    @classmethod
    def fromJson(cls, json_str: str):
        data = json.loads(json_str)
        return cls.fromDict(data)

    def toJson(self) -> str:
        return json.dumps(self.toDict())
