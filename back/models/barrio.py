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
        self.nodos = {}

    def agregarNodo(self, nodo):
        if nodo not in self.nodos:
            self.nodos[nodo] = []

    def agregarArista(self, nodo, arista):
        if nodo in self.nodos:
            self.nodos[nodo].append(arista)
        else:
            self.nodos[nodo] = [arista]

    def toJson(self):
        return json.dumps(self.nodos, default=lambda o: o.__dict__, indent=4)
    
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
        return {nodo: [arista.__dict__ for arista in aristas] for nodo, aristas in self.nodos.items()}

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
    
    def dijkstra(self, start):
        distances = {nodo.id: float('infinity') for nodo in self.nodos}
        distances[start.id] = 0
        previous_nodes = {nodo.id: None for nodo in self.nodos}
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node.id]:
                continue
            for arista in self.nodos[current_node]:
                if arista.obstruido:
                    continue
                distance = current_distance + arista.flujo
                if distance < distances[arista.nodo.id]:
                    distances[arista.nodo.id] = distance
                    previous_nodes[arista.nodo.id] = (current_node, arista)
                    heapq.heappush(priority_queue, (distance, arista.nodo))
        return distances, previous_nodes

    def shortestPathsFromTanks(self):
        tank_nodes = [nodo for nodo in self.nodos if nodo.tank]
        self.shortest_paths = {}
        for tank_node in tank_nodes:
            distances, previous_nodes = self.dijkstra(tank_node)
            paths = {}
            for nodo_id in distances:
                path = []
                current_id = nodo_id
                while previous_nodes[current_id] is not None:
                    current_node, arista = previous_nodes[current_id]
                    path.insert(0, arista)
                    current_id = current_node.id
                paths[nodo_id] = path
            self.shortest_paths[tank_node.id] = paths
        return self.shortest_paths
    
    def maxFlow(self, source, sink):
        def bfs(source, sink, parent):
            visited = {nodo: False for nodo in self.nodos}
            queue = [source]
            visited[source] = True
            while queue:
                current_node = queue.pop(0)
                for arista in self.nodos[current_node]:
                    if not visited[arista.nodo] and arista.flujoOptimo > 0:
                        queue.append(arista.nodo)
                        visited[arista.nodo] = True
                        parent[arista.nodo] = (current_node, arista)
                        if arista.nodo == sink:
                            return True
            return False

        parent = {}
        max_flow = 0

        while bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, parent[s][1].flujoOptimo)
                s = parent[s][0]

            max_flow += path_flow

            while v != source:
                u, arista = parent[v]
                arista.flujoOptimo -= path_flow
                reverse_arista = next((a for a in self.nodos[v] if a.nodo == u), None)
                if reverse_arista:
                    reverse_arista.flujoOptimo += path_flow
                else:
                    self.nodos[v].append(Arista(u, path_flow, False))
                v = u
        return max_flow