import json
from back.models.arista import Arista
from back.models.nodo import Nodo
from back.models.barrio import Barrio
from back.models.aristaBarrio import AristaBarrio
class BaseDatos:
    def __init__(self):
        self.data = {"nodos": {}, "barrios": {}, "red": {}}

    def almacenarNodo(self, nodo: Nodo):
        self.data["nodos"][nodo.id] = nodo.toDict()

    def almacenarArista(self, arista: Arista, barrio_id: str, nodo_id: str):
        if nodo_id in self.data["barrios"][barrio_id]:
            self.data["barrios"][barrio_id][nodo_id].append(arista.toDict())
        else:
            self.data["barrios"][barrio_id][nodo_id] = [arista.toDict()]

    def almacenarBarrio(self, barrio_id: str, barrio: Barrio):
        self.data["barrios"][barrio_id] = barrio.toDict()
        self.data["red"][barrio_id] = []

    def almacenarAristaBarrio(self, arista: AristaBarrio):
        tankId = arista.tankId
        nodo = self.data["nodos"][tankId]
        if(nodo is None):
            raise ValueError(f"Tank ID {tankId} not found in any node.")
        if(nodo["tank"] is None):
            raise ValueError(f"Tank ID {tankId} not found in any node.")
        barrioIdFrom = None
        for barrioId, barrio in self.data["barrios"].items():
            if tankId in barrio:
                barrioIdFrom = barrioId
        if not barrioIdFrom:
            raise ValueError(f"Tank ID {tankId} not found in any neighborhood.")
        if barrioIdFrom == arista.barrioId:
            raise ValueError(f"Tank ID {tankId} is already in neighborhood {barrioIdFrom}.")        
        if barrioIdFrom in self.data["red"]:
            self.data["red"][barrioIdFrom].append(arista.toDict())
        else:
            self.data["red"][barrioIdFrom] = [arista.toDict()]

    def guardarEnArchivo(self, archivo: str):
        with open(archivo, "w") as file:
            json.dump(self.data, file, indent=4)

    def cargarDesdeArchivo(self, archivo: str):
        with open(archivo, "r") as file:
            self.data = json.load(file)

    def obtenerDatos(self):
        return self.data