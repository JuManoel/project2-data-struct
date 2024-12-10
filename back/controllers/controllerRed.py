from back.services.serviceRed import ServiceRed
from back.models.nodo import Nodo
from back.models.tank import Tank
from back.models.arista import Arista
from back.models.barrio import Barrio

class ControllerRed:
    def __init__(self):
        self.serviceRed = ServiceRed()

    def crearNodo(self, id: str, tank=None):
        """Crear un nuevo nodo y almacenarlo."""
        nodo = Nodo(id, tank)
        self.serviceRed.agregarNodo(nodo)
        return {"message": "Nodo creado exitosamente", "nodo": nodo.toDict()}

    def crearTanque(self, capacidad: float, capacidadTotal: float):
        """Crear un nuevo tanque y almacenarlo."""
        tanque = Tank(capacidad, capacidadTotal)
        self.serviceRed.agregarTanque(tanque)
        return {"message": "Tanque creado exitosamente", "tanque": tanque.toDict()}

    def crearArista(self, nodo1_id: str, nodo2_id: str, flujoOptimo: float):
        """Crear una nueva arista entre dos nodos."""
        arista = self.serviceRed.crearArista(nodo1_id, nodo2_id, flujoOptimo)
        return {"message": "Arista creada exitosamente", "arista": arista.toDict()}

    def crearBarrio(self, barrio_id: str):
        """Crear un nuevo barrio y almacenarlo."""
        barrio = Barrio(barrio_id)
        self.serviceRed.agregarBarrio(barrio)
        return {"message": "Barrio creado exitosamente", "barrio": barrio.toDict()}

    def obtenerDatos(self):
        """Obtener todos los datos de la red."""
        data = self.serviceRed.obtenerDatos()
        return {"message": "Datos obtenidos exitosamente", "data": data}

    def cargarDesdeArchivo(self, archivo: str):
        """Cargar datos desde un archivo JSON."""
        self.serviceRed.cargarDesdeArchivo(archivo)
        return {"message": f"Datos cargados desde {archivo}"}

    def guardarEnArchivo(self, archivo: str):
        """Guardar todos los datos en un archivo JSON."""
        self.serviceRed.guardarEnArchivo(archivo)
        return {"message": f"Datos guardados en {archivo}"}
