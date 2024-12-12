from back.models.nodo import Nodo
from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.BaseDatos import BaseDatos
from back.models.aristaBarrio import AristaBarrio
class ControllerRed:
    def __init__(self):
        self.baseDatos = BaseDatos()

    def crearNodo(self, id: str, tank=None):
        """Crear un nuevo nodo y almacenarlo."""
        nodo = Nodo(id, tank)
        self.baseDatos.almacenarNodo(nodo)
        return {"message": "Nodo creado exitosamente", "nodo": nodo.toDict()}

    def crearArista(self, flujo: int, nodoIdTo: str, obstruido: int, flujoOptimo: int, barrioId: str, nodoIdFrom: str): 
        """Crear una nueva arista entre dos nodos."""
        arista = Arista(flujo, nodoIdTo, obstruido, flujoOptimo)
        self.baseDatos.almacenarArista(arista, barrioId, nodoIdFrom)
        return {"message": "Arista creada exitosamente", "arista": arista.toDict()}

    def crearBarrio(self, barrio_id: str):
        """Crear un nuevo barrio y almacenarlo."""
        barrio = Barrio(barrio_id)
        self.baseDatos.almacenarBarrio(barrio_id,barrio)
        return {"message": "Barrio creado exitosamente", "barrio": barrio.toDict()}
    def crearAristaBarrio(self, flujo: int, tankId: str, obstruido: int, barrioId: str, nodoId: str, flujoOptimo: int):
        """Crear una nueva arista entre dos nodos."""
        arista = AristaBarrio(flujo, tankId, obstruido, barrioId, nodoId, flujoOptimo)
        self.baseDatos.almacenarAristaBarrio(arista)
        return {"message": "Arista creada exitosamente", "arista": arista.toDict()}
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
