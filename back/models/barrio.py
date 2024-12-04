from back.models.nodo import Nodo
from back.models.arista import Arista
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
    def __init__(self):
        self.nodos = {}  # Initialize nodos as a dictionary
        self.aristasBarrio = {}
        self.tanques = {}
    def agregarNodo(self, nodo : Nodo):
        if nodo not in self.nodos:
            self.nodos[nodo] = []

    def agregarArista(self, nodo:Nodo, arista:Arista):
        if nodo in self.nodos:
            self.nodos[nodo].append(arista)
        else:
            self.nodos[nodo] = [arista]
    def toJson(self):
        # Convert Nodo keys to their IDs (strings) before serialization
        nodos_serializable = {nodo.id: {k: v.toDict() if isinstance(v, Tank) else v for k, v in nodo.__dict__.items()} for nodo in self.nodos}
        return json.dumps(nodos_serializable, indent=4, default=lambda o: o.__dict__)
    
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
        return {nodo.id: [arista.toDict() for arista in aristas] for nodo, aristas in self.nodos.items()}

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
    
    def dijkstra(self, start: Nodo) -> "Barrio":
        # Inicializar estructuras
        distances = {nodo.id: float('inf') for nodo in self.nodos}
        distances[start.id] = 0
        previous_nodes = {nodo.id: None for nodo in self.nodos}
        visited = set()
        heap = [(0, start)]
    
        # Algoritmo principal
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_node in visited:
                continue
            visited.add(current_node)
            
            for arista in self.nodos[current_node]:
                neighbor = arista.nodo
                distance = current_distance + arista.flujo
                if distance < distances[neighbor.id]:
                    distances[neighbor.id] = distance
                    previous_nodes[neighbor.id] = (current_node, arista)
                    heapq.heappush(heap, (distance, neighbor))
        
        # Crear un subgrafo con solo las aristas recorridas
        subgrafo = Barrio()
        for nodo_id in distances:
            # Agregar el nodo actual al subgrafo
            current_node = Nodo(id=nodo_id)
            subgrafo.agregarNodo(current_node)
            
            # Agregar la arista que llevó al nodo actual, si existe
            if previous_nodes[nodo_id] is not None:
                previous_node, arista = previous_nodes[nodo_id]
                subgrafo.agregarNodo(previous_node)
                subgrafo.agregarArista(previous_node, arista)

        return subgrafo

    def shortestPathsFromTanks(self):
        tank_nodes = [nodo for nodo in self.nodos if nodo.tank]
        new_graph = Barrio()
        for tank_node in tank_nodes:
            distances, previous_nodes = self.dijkstra(tank_node)
            for nodo_id in distances:
                if nodo_id not in new_graph.nodos:
                    new_graph.agregarNodo(Nodo(id=nodo_id))
                path = []
                current_id = nodo_id
                while previous_nodes[current_id] is not None:
                    current_node, arista = previous_nodes[current_id]
                    path.insert(0, arista)
                    current_id = current_node.id
                for arista in path:
                    new_graph.agregarArista(Nodo(id=current_id), arista)
        return new_graph
    
