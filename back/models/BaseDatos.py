import json

class BaseDatos:
    def __init__(self):
        self.data = {"nodos": {}, "aristas": {}, "barrios": {}, "tanques": {}}

    def almacenarNodo(self, nodo: Nodo):
        self.data["nodos"][nodo.id] = nodo.toDict()

    def almacenarArista(self, arista: Arista):
        arista_id = f"{arista.nodo.id}-{arista.flujoOptimo}"
        self.data["aristas"][arista_id] = arista.toDict()

    def almacenarBarrio(self, barrio_id: str, barrio: Barrio):
        self.data["barrios"][barrio_id] = barrio.toDict()

    def almacenarTanque(self, tanque_id: str, tanque: Tank):
        self.data["tanques"][tanque_id] = tanque.toDict()

    def guardarEnArchivo(self, archivo: str):
        with open(archivo, "w") as file:
            json.dump(self.data, file, indent=4)

    def cargarDesdeArchivo(self, archivo: str):
        with open(archivo, "r") as file:
            self.data = json.load(file)

    def obtenerDatos(self):
        return self.data