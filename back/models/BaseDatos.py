import json
from back.models.arista import Arista
from back.models.nodo import Nodo
from back.models.barrio import Barrio
from back.models.aristaBarrio import AristaBarrio
from back.models.red import Red
class BaseDatos:
    def __init__(self):
        self.data = {"nodos": {}, "barrios": {}, "red": {}, "barriosOptimos": {}, "redOptima": {}}

    def almacenarNodo(self, nodo: Nodo, barrio_id: str):
        self.data["nodos"][nodo.id] = nodo.toDict()
        self.data["barrios"][barrio_id][nodo.id] = []

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

    def optimizarBarrio(self, barrio_id: str):
        barrio = Barrio(barrio_id)
        nodos_con_tanque = [nodo_id for nodo_id, nodo in self.data["nodos"].items() if nodo["tank"] is not None]
        barrio.barrio = self.data["barrios"][barrio_id]
        barrioOptimo = barrio.optimizar(nodos_con_tanque)
        self.data["barriosOptimos"][barrio_id] = barrioOptimo.toDict()
        return barrioOptimo

    def optimizarRed(self):
        for barrio_id in self.data["barrios"]:
            self.optimizarBarrio(barrio_id)
        redOptima = Red()
        redOptima.red = self.data["red"]
        redOptima.optimizar()
        self.data["redOptima"] = redOptima.toDict()
        return redOptima

    def guardarEnArchivo(self, archivo: str):
        with open(archivo, "w") as file:
            json.dump(self.data, file, indent=4)

    def cargarDesdeArchivo(self, archivo: str):
        with open(archivo, "r") as file:
            self.data = json.load(file)

    def obtenerDatos(self):
        return self.data