from back.models.nodo import Nodo
from back.models.tank import Tank
from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.BaseDatos import BaseDatos

class ControllerRed:
    def __init__(self):
        self.baseDatos = BaseDatos()

    def crearNodo(self, id: str, tank=None):
        """Crear un nuevo nodo y almacenarlo."""
        if isinstance(tank, dict):
            tank = Tank.fromDict(tank)
        nodo = Nodo(id, tank)
        self.baseDatos.almacenarNodo(nodo)
        return {"message": "Nodo creado exitosamente", "nodo": nodo.toDict()}

    def crearTanque(self, id: str,capacidad: float, capacidadTotal: float):
        """Crear un nuevo tanque y almacenarlo."""
        tanque = Tank(capacidad, capacidadTotal)
        self.baseDatos.almacenarTanque(id,tanque)
        return {"message": "Tanque creado exitosamente", "tanque": tanque.toDict()}

    def crearArista(self, flujo: int, nodo: Nodo, obstruido: int, flujoOptimo: int):
        """Crear una nueva arista entre dos nodos."""
        if(nodo["tank"] != None):
            if(isinstance(nodo["tank"], dict)):
                nodo["tank"] = Tank.fromDict(nodo["tank"])
        if isinstance(nodo, dict):
            nodo = Nodo.fromDict(nodo)
        arista = Arista(flujo, nodo, obstruido, flujoOptimo)
        self.baseDatos.almacenarArista(arista)
        return {"message": "Arista creada exitosamente", "arista": arista.toDict()}

    def crearBarrio(self, barrio_id: str):
        """Crear un nuevo barrio y almacenarlo."""
        barrio = Barrio(barrio_id)
        self.baseDatos.almacenarBarrio(barrio_id,barrio)
        return {"message": "Barrio creado exitosamente", "barrio": barrio.toDict()}

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
