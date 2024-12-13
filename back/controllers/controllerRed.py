from back.models.nodo import Nodo
from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.BaseDatos import BaseDatos
from back.models.aristaBarrio import AristaBarrio
class ControllerRed:
    def __init__(self):
        self.baseDatos = BaseDatos()

    def crearNodo(self, id: str, tank=None, barrioId=None):
        """Crear un nuevo nodo y almacenarlo."""
        nodo = Nodo(id, tank)
        self.baseDatos.almacenarNodo(nodo, barrioId)
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
    def crearObstrucion(self, nodoFrom: str, nodoTo: str, nivel: int):
        """Crear una obstrucción en un nodo."""
        self.baseDatos.crearObstruccion(nodoFrom, nodoTo, nivel)
        return {"message": "Obstrucción creada exitosamente"}
    def optimizarBarrio(self, barrioId: str):
        barrioOprimo = self.baseDatos.optimizarBarrio(barrioId)
        return {"message": "Barrio optimizado exitosamente", "barrioOptimo": barrioOprimo.toDict()}

    def optimizarRed(self):
        redOptima = self.baseDatos.optimizarRed()
        return {"message": "Red optimizada exitosamente", "redOptima": redOptima.toDict()}

    def eliminarArista(self, barrioId: str, nodoIdFrom: str, nodoIdTo: str):
        """Eliminar una arista entre dos nodos."""
        self.baseDatos.eliminarArista(barrioId, nodoIdFrom, nodoIdTo)
        return {"message": "Arista eliminada exitosamente"}

    def eliminarNodo(self, barrioId: str, nodoId: str):
        """Eliminar un nodo."""
        self.baseDatos.eliminarNodo(barrioId, nodoId)
        return {"message": "Nodo eliminado exitosamente"}

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
