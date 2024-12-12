import json
from back.models.arista import Arista
from back.models.nodo import Nodo
from back.models.barrio import Barrio
class BaseDatos:
    def __init__(self):
        self.data = {"nodos": {}, "aristas": {}, "barrios": {}}

    def almacenarNodo(self, nodo: Nodo):
        self.data["nodos"][nodo.id] = nodo.toDict()

    def almacenarArista(self, arista: Arista, barrio_id: str, nodo_id: str):
        if nodo_id in self.data["barrios"][barrio_id]:
            self.data["barrios"][barrio_id][nodo_id].append(arista.toDict())
        else:
            self.data["barrios"][barrio_id][nodo_id] = [arista.toDict()]

    def almacenarBarrio(self, barrio_id: str, barrio: Barrio):
        self.data["barrios"][barrio_id] = barrio.toDict()

    def guardarEnArchivo(self, archivo: str):
        with open(archivo, "w") as file:
            json.dump(self.data, file, indent=4)

    def cargarDesdeArchivo(self, archivo: str):
        with open(archivo, "r") as file:
            self.data = json.load(file)

    def obtenerDatos(self):
        return self.data