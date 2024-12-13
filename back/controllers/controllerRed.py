import json
from back.models.nodo import Nodo
from back.models.arista import Arista
from back.models.barrio import Barrio
from back.models.BaseDatos import BaseDatos
from back.models.aristaBarrio import AristaBarrio

class ControllerRed:
    def __init__(self):
        self.baseDatos = BaseDatos()
        try:
            self.reporte = open('reporte.txt', 'a')
        except FileNotFoundError:
            self.reporte = open('reporte.txt', 'w')

    def crearNodo(self, id: str, tank=None, barrioId=None):
        """Crear un nuevo nodo y almacenarlo."""
        nodo = Nodo(id, tank)
        self.baseDatos.almacenarNodo(nodo, barrioId)
        result = {"message": "Nodo creado exitosamente", "nodo": nodo.toDict()}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def crearArista(self, flujo: int, nodoIdTo: str, obstruido: int, flujoOptimo: int, barrioId: str, nodoIdFrom: str): 
        """Crear una nueva arista entre dos nodos."""
        arista = Arista(flujo, nodoIdTo, obstruido, flujoOptimo)
        self.baseDatos.almacenarArista(arista, barrioId, nodoIdFrom)
        result = {"message": "Arista creada exitosamente", "arista": arista.toDict()}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def crearBarrio(self, barrio_id: str):
        """Crear un nuevo barrio y almacenarlo."""
        barrio = Barrio(barrio_id)
        self.baseDatos.almacenarBarrio(barrio_id, barrio)
        result = {"message": "Barrio creado exitosamente", "barrio": barrio.toDict()}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def crearAristaBarrio(self, flujo: int, tankId: str, obstruido: int, barrioId: str, nodoId: str, flujoOptimo: int):
        """Crear una nueva arista entre dos nodos."""
        arista = AristaBarrio(flujo, tankId, obstruido, barrioId, nodoId, flujoOptimo)
        self.baseDatos.almacenarAristaBarrio(arista)
        result = {"message": "Arista creada exitosamente", "arista": arista.toDict()}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def crearObstrucion(self, nodoFrom: str, nodoTo: str, nivel: int):
        """Crear una obstrucción en un nodo."""
        self.baseDatos.crearObstruccion(nodoFrom, nodoTo, nivel)
        result = {"message": "Obstrucción creada exitosamente"}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def optimizarBarrio(self, barrioId: str):
        barrioOprimo = self.baseDatos.optimizarBarrio(barrioId)
        result = {"message": "Barrio optimizado exitosamente", "barrioOptimo": barrioOprimo.toDict()}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def optimizarRed(self):
        redOptima = self.baseDatos.optimizarRed()
        result = {"message": "Red optimizada exitosamente", "redOptima": redOptima.toDict()}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def eliminarArista(self, barrioId: str, nodoIdFrom: str, nodoIdTo: str):
        """Eliminar una arista entre dos nodos."""
        self.baseDatos.eliminarArista(barrioId, nodoIdFrom, nodoIdTo)
        result = {"message": "Arista eliminada exitosamente"}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def eliminarNodo(self, barrioId: str, nodoId: str):
        """Eliminar un nodo."""
        self.baseDatos.eliminarNodo(barrioId, nodoId)
        result = {"message": "Nodo eliminado exitosamente"}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def obtenerDatos(self):
        """Obtener todos los datos de la red."""
        data = self.baseDatos.obtenerDatos()
        result = {"message": "Datos obtenidos exitosamente", "data": data}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def cargarDesdeArchivo(self, archivo: str):
        """Cargar datos desde un archivo JSON."""
        self.baseDatos.cargarDesdeArchivo(archivo)
        result = {"message": f"Datos cargados desde {archivo}"}
        self.reporte.write(json.dumps(result) + '\n')
        return result

    def guardarEnArchivo(self, archivo: str):
        """Guardar todos los datos en un archivo JSON."""
        self.baseDatos.guardarEnArchivo(archivo)
        result = {"message": f"Datos guardados en {archivo}"}
        self.reporte.write(json.dumps(result) + '\n')
        return result
