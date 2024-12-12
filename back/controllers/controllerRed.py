from back.models.nodo import Nodo
from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.BaseDatos import BaseDatos

class ControllerRed:
    def __init__(self):
        self.baseDatos = BaseDatos()

    def crearNodo(self, id: str, tank=None):
        """Crear un nuevo nodo y almacenarlo."""
        nodo = Nodo(id, tank)
        self.baseDatos.almacenarNodo(nodo)
        return {"message": "Nodo creado exitosamente", "nodo": nodo.toDict()}

    def crearArista(self, flujo: int, nodoIdTo: str, obstruido: int, flujoOptimo: int, barrioId: str, nodoIdFrom: str): 
        print(flujo, nodoIdTo, obstruido, flujoOptimo)
        """Crear una nueva arista entre dos nodos."""
        arista = Arista(flujo, nodoIdTo, obstruido, flujoOptimo)
        self.baseDatos.almacenarArista(arista, barrioId, nodoIdFrom)
        return {"message": "Arista creada exitosamente", "arista": arista.toDict()}

    def crearBarrio(self, barrio_id: str):
        """Crear un nuevo barrio y almacenarlo."""
        barrio = Barrio(barrio_id)
        self.baseDatos.almacenarBarrio(barrio_id,barrio)
        return {"message": "Barrio creado exitosamente", "barrio": barrio.toDict()}

    def adicionarNodoBarrio(self, barrio_id: str, nodo_id: str):
        """Adicionar un nodo a un barrio."""
        barrio = self.baseDatos.data["barrios"][barrio_id]
        barrio["nodos"].append(nodo_id)
        return {"message": "Nodo añadido al barrio exitosamente", "barrio": barrio.toDict()}

    def adicionarAristaBarrio(self, barrio_id: str, nodo_id: str, arista_id: str):
        """Adicionar una arista a un nodo en un barrio."""
        barrio = self.baseDatos.data["barrios"][barrio_id]
        nodo = barrio["nodos"][nodo_id]
        nodo["aristas"].append(arista_id)
        return {"message": "Arista añadida al nodo exitosamente", "barrio": barrio.toDict()}

    def obtenerDatos(self):
        """Obtener todos los datos de la red."""
        data = self.baseDatos.obtenerDatos()
        return {"message": "Datos obtenidos exitosamente", "data": data}

    def cargarDesdeArchivo(self, archivo: str):
        """Cargar datos desde un archivo JSON."""
        self.baseDatos.cargarDesdeArchivo(archivo)
        return {"message": f"Datos cargados desde {archivo}"}

    def guardarEnArchivo(self, archivo: str):
        """Guardar todos los datos en un archivo JSON."""
        self.baseDatos.guardarEnArchivo(archivo)
        return {"message": f"Datos guardados en {archivo}"}
