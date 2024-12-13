from back.models.arista import Arista
from back.models.nodo import Nodo

import json
import heapq

class Barrio:
    """
    A class to represent a neighborhood (Barrio) with nodes and edges.
    Attributes
    ----------
    nodos : dict
        A dictionary to store nodes and their corresponding edges.
    Methods
    -------
    agregarNodo(nodo):
        Adds a node to the neighborhood if it does not already exist.
    agregarArista(nodo, arista):
        Adds an edge to a node in the neighborhood.
    toJson():
        Converts the neighborhood data to a JSON string.
    fromJson(json_str):
        Creates a Barrio instance from a JSON string.
    toDict():
        Converts the neighborhood data to a dictionary.
    fromDict(dict_data):
        Creates a Barrio instance from a dictionary.
    dijkstra(start):
        Computes the shortest paths from a starting node using Dijkstra's algorithm.
    shortestPathsFromTanks():
        Computes the shortest paths from all nodes that have a tank.
    """
    def __init__(self, id):
        self.id = id
        self.barrio = {}
    def agregarNodo(self, nodoId : str):
        if nodoId not in self.barrio:
            self.barrio[nodoId] = []

    def agregarArista(self, nodoId:str, arista:Arista):
        if nodoId in self.barrio:
            self.barrio[nodoId].append(arista)
        else:
            self.barrio[nodoId] = [arista]

    def toJson(self):
        return json.dumps(self.toDict())

    @classmethod
    def fromJson(cls, json_str):
        data = json.loads(json_str)
        barrio = cls()
        for nodo, aristas in data.items():
            nodo_obj = Nodo(**nodo)
            barrio.agregarNodo(nodo_obj)
            for arista in aristas:
                arista_obj = Arista(**arista)
                barrio.agregarArista(nodo_obj, arista_obj)
        return barrio

    def toDict(self):
        return {nodo: [arista.toDict() for arista in aristas] for nodo, aristas in self.barrio.items()}

    @classmethod
    def fromDict(cls, dict_data):
        barrio = cls()
        for nodo, aristas in dict_data.items():
            nodo_obj = Nodo(**nodo)
            barrio.agregarNodo(nodo_obj)
            for arista in aristas:
                arista_obj = Arista(**arista)
                barrio.agregarArista(nodo_obj, arista_obj)
        return barrio
    def dijkstra(self, start: str):
        # Inicializar estructuras
        distances = {nodo: float('inf') for nodo in self.barrio}
        distances[start] = 0
        previous_nodes = {nodo: None for nodo in self.barrio}
        visited = set()
        heap = [(0, start)]  # (distancia, nodo)

        # Algoritmo principal
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_node in visited:
                continue
            visited.add(current_node)

            for arista in self.barrio[current_node]:  # Iterar sobre las aristas
                neighbor = arista["nodoId"]
                distance = current_distance + arista["flujo"]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = (current_node, arista)
                    heapq.heappush(heap, (distance, neighbor))

        return distances, previous_nodes  # Retornar diccionarios

    def shortestPathsFromTanks(self, tankes):
        tank_nodes = [nodo for nodo in self.barrio if nodo in tankes]
        if not tank_nodes:
            raise ValueError("No hay tanques en el barrio")

        distances_from_tanks = {tank: {} for tank in tank_nodes}
        paths_from_tanks = {tank: {} for tank in tank_nodes}

        for tank in tank_nodes:
            distances, previous_nodes = self.dijkstra(tank)
            distances_from_tanks[tank] = distances
            paths_from_tanks[tank] = previous_nodes

        # Asignación de nodos a tanques
        nodo_a_tanque = {}
        for nodo in self.barrio:
            min_distance = float('inf')
            assigned_tank = None
            for tank_id, distances in distances_from_tanks.items():
                if nodo in distances and distances[nodo] < min_distance:
                    min_distance = distances[nodo]
                    assigned_tank = tank_id
            if assigned_tank is not None:
                nodo_a_tanque[nodo] = assigned_tank

        # Construcción del subgrafo
        subgrafo = Barrio(self.id)
        for nodo_id, tank_id in nodo_a_tanque.items():
            subgrafo.agregarNodo(nodo_id)

            # Reconstrucción del camino hacia el tanque
            current_id = nodo_id
            while current_id != tank_id:
                if isinstance(paths_from_tanks[tank_id][current_id], tuple):
                    previous_node, arista = paths_from_tanks[tank_id][current_id]
                    subgrafo.agregarNodo(previous_node)
                    subgrafo.agregarArista(previous_node, Arista(**arista))
                    current_id = previous_node
                else:
                    raise ValueError("No se encontró un camino hacia el tanque")
                    break
        return subgrafo
    def menorFlujo(self):
        menorFlujo = float('inf')
        for nodo in self.barrio:
            for arista in self.barrio[nodo]:
                if arista["flujo"] < menorFlujo:
                    menorFlujo = arista["flujo"]
        return menorFlujo
    
    def optimizar(self, nodosTanks):
        grafoOptimo = self.shortestPathsFromTanks(nodosTanks)
        menorFlujo = self.menorFlujo()
        for nodo in grafoOptimo.barrio:
            for arista in grafoOptimo.barrio[nodo]:
                arista.flujoOptimo = menorFlujo
        return grafoOptimo