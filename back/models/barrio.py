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
            self.nodos[nodoId].append(arista)
        else:
            self.nodos[nodoId] = [arista]

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

    def dijkstra(self, start: Nodo):
        # Inicializar estructuras
        distances = {nodo.id: float('inf') for nodo in self.nodos}
        distances[start.id] = 0
        previous_nodes = {nodo.id: None for nodo in self.nodos}
        visited = set()
        heap = [(0, start)]  # (distancia, nodo)

        # Algoritmo principal
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_node in visited:
                continue
            visited.add(current_node)

            for arista in self.nodos[current_node]:  # Iterar sobre las aristas
                neighbor = arista.nodo
                distance = current_distance + arista.flujo
                if distance < distances[neighbor.id]:
                    distances[neighbor.id] = distance
                    previous_nodes[neighbor.id] = (current_node, arista)
                    heapq.heappush(heap, (distance, neighbor))

        return distances, previous_nodes  # Retornar diccionarios

    def shortestPathsFromTanks(self):
        tank_nodes = [nodo for nodo in self.nodos if nodo.tank]
        if not tank_nodes:
            print("No se encontraron tanques.")
            return Barrio(self.id)  # Retornar un barrio vacío si no hay tanques

        distances_from_tanks = {tank.id: {} for tank in tank_nodes}
        paths_from_tanks = {tank.id: {} for tank in tank_nodes}

        for tank in tank_nodes:
            print(f"Ejecutando Dijkstra desde el tanque: {tank.id}")
            distances, previous_nodes = self.dijkstra(tank)
            distances_from_tanks[tank.id] = distances
            paths_from_tanks[tank.id] = previous_nodes

        # Asignación de nodos a tanques
        nodo_a_tanque = {}
        for nodo in self.nodos:
            min_distance = float('inf')
            assigned_tank = None
            for tank_id, distances in distances_from_tanks.items():
                if nodo.id in distances and distances[nodo.id] < min_distance:
                    min_distance = distances[nodo.id]
                    assigned_tank = tank_id
            if assigned_tank is not None:
                nodo_a_tanque[nodo.id] = assigned_tank

        # Construcción del subgrafo
        subgrafo = Barrio(self.id)
        for nodo_id, tank_id in nodo_a_tanque.items():
            nodo = Nodo(id=nodo_id)
            subgrafo.agregarNodo(nodo)

            # Reconstrucción del camino hacia el tanque
            current_id = nodo_id
            while current_id != tank_id:
                if isinstance(paths_from_tanks[tank_id][current_id], tuple):
                    previous_node, arista = paths_from_tanks[tank_id][current_id]
                    subgrafo.agregarNodo(previous_node)
                    subgrafo.agregarArista(previous_node, arista)
                    current_id = previous_node.id
                else:
                    print(f"Error: Expected tuple, but got {paths_from_tanks[tank_id][current_id]}")
                    break

        return subgrafo