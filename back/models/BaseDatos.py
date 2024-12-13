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
        red = Red()
        red.red = self.data["red"]
        redOptima = red.optimizar()
        self.data["redOptima"] = redOptima.toDict()
        return redOptima

    def eliminarArista(self, barrio_id: str, nodo_id_from: str, nodo_id_to: str):
        barrio = Barrio(barrio_id)
        barrio.barrio = self.data["barrios"][barrio_id]
        aux = False
        for arista in barrio.barrio[nodo_id_from]:
            if arista["nodoId"] == nodo_id_to:
                barrio.barrio[nodo_id_from].remove(arista)
                aux = True
        if(not aux):
            red = Red.fromDict(self.data["red"])
            for arista in red.red[barrio_id]:
                if arista["nodoIdFrom"] == nodo_id_from and arista["nodoIdTo"] == nodo_id_to:
                    red.red[barrio_id].remove(arista)
                    self.data["red"] = red.toDict()
                    aux = True
        if(not aux):
            raise ValueError(f"Edge from {nodo_id_from} to {nodo_id_to} not found in neighborhood {barrio_id}.")
        self.data["barrios"][barrio_id] = barrio.barrio
    
    def eliminarNodo(self, barrio_id: str, nodo_id: str):
        barrio = Barrio(barrio_id)
        barrio.barrio = self.data["barrios"][barrio_id]
        del barrio.barrio[nodo_id]
        self.data["barrios"][barrio_id] = barrio.barrio

        del self.data["nodos"][nodo_id]
        for nodoId, aristas in self.data["barrios"][barrio_id].items():
            for arista in aristas:
                if arista["nodoId"] == nodo_id:
                    aristas.remove(arista)
                    self.data["barrios"][barrio_id][nodoId] = aristas
        for barrio_id, aristaBarrio in self.data["red"].items():
            for arista in aristaBarrio:
                if arista["nodoId"] == nodo_id:
                    aristaBarrio.remove(arista)
                    self.data["red"][barrio_id] = aristaBarrio

    def crearObstruccion(self, nodo_id_from: str, nodo_id_to: str, nivel: int):
        arista = None
        for _, barrio in self.data["barrios"].items():
            if nodo_id_from in barrio:
                for arista in barrio[nodo_id_from]:
                    if arista["nodoId"] == nodo_id_to:
                        arista["obstruido"] = nivel
                        break
        if arista is None:
            for _, aristaBarrio in self.data["red"].items():
                for arista in aristaBarrio:
                    if arista["tankId"] == nodo_id_from and arista["nodoId"] == nodo_id_to:
                        arista["obstruido"] = nivel

    def guardarEnArchivo(self, archivo: str):
        with open(archivo, "w") as file:
            json.dump(self.data, file, indent=4)

    def cargarDesdeArchivo(self, archivo: str):
        with open(archivo, "r") as file:
            self.data = json.load(file)

    def obtenerDatos(self):
        return self.data