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
    def almacenarAristaBarrio(self, arista: AristaBarrio):
        print(arista)
        arista_id = f"{arista.tank}-{arista.flujoOptimo}"
        self.data["aristasBarrio"][arista_id] = arista.toDict()

    def crearAristaBarrio(self, flujo: float, idTank: str, obstruido: int, barrio: str, idNodo: str, flujoOptimo: float):
        """Crear una nueva arista entre dos nodos en un barrio."""
        arista = AristaBarrio(flujo, idTank, obstruido, barrio, idNodo, flujoOptimo)
        self.almacenarAristaBarrio(arista)

    
    def adicionarAristaEnRed(self, barrio_id: str, arista: AristaBarrio,):
        print(arista)
        """Adicionar una arista a la red."""
        if barrio_id not in self.data["red"]:
            self.data["red"][barrio_id] = [arista]
        else:

            self.data["red"][barrio_id].append(arista)
        if arista["barrio"] not in self.data["red"]:
            self.data["red"][arista["barrio"]] = []
        return self.data["red"]

    def almacenarBarrio(self, barrio: Barrio):
     if not barrio.id:
        raise ValueError("El barrio debe tener un ID válido.")

     if barrio.id in self.data["barrios"]:
        raise ValueError(f"El barrio con ID {barrio.id} ya existe en la base de datos.")

     self.data["barrios"][barrio.id] = barrio.toDict()

    def crearRed(self, red: Red):
        self.data["red"] = red.toDict

    def crearRedCompleta(barrio: Barrio):
        red = {"barrios": {}}

    # Iterar sobre cada nodo del barrio
        red["barrios"][barrio.id] = {}

        for nodo_id, aristas in barrio.aristasBarrio.items():
            red["barrios"][barrio.id][nodo_id] = []

        # Iterar sobre las aristas del nodo
            for arista in aristas:
                nodo_destino = arista.nodo.toDict()
                arista_dict = {
                    "flujo": arista.flujo,
                    "nodo": nodo_destino,
                    "obstruido": arista.obstruido,
                    "flujoOptimo": arista.flujoOptimo
                }
                red["barrios"][barrio.id][nodo_id].append(arista_dict)
        return red
    def crearNodo(self, nodo_id: str, tanque: dict, barrio_id: str):
        """Crear un nodo con los datos proporcionados."""
        nodo = Nodo(id=nodo_id, tanque=Tank(**tanque), barrio_id=barrio_id)
        self.almacenarNodo(nodo)
        return {"nodo": nodo}

    def crearArista(self, flujo: int, nodo: Nodo, obstruido: int, flujoOptimo: int, barrio_id: str):
        """Crear una arista con los datos proporcionados."""
        arista = Arista(flujo=flujo, nodo=nodo, obstruido=obstruido, flujoOptimo=flujoOptimo, barrio_id=barrio_id)
        self.almacenarArista(arista)
        return {"arista": arista}

    def obtenerBarrio(self, barrio_id: str):
        """Obtener un barrio por su ID."""
        return self.data["barrios"].get(barrio_id)

    def actualizarBarrio(self, barrio: Barrio):
        """Actualizar un barrio en la base de datos."""
        self.data["barrios"][barrio.id] = barrio.toDict()
