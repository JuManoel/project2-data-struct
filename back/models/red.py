from back.models.barrio import Barrio
from back.models.aristaBarrio import AristaBarrio
import json
import heapq

class Red:
    def __init__(self):
        self.red = {}

    def agregarBarrio(self, barrioId):
        if barrioId not in self.red:
            self.red[barrioId] = []

    def agregarArista(self, barrioId, arista: AristaBarrio):
        if barrioId in self.red:
            self.red[barrioId].append(arista)
        else:
            self.red[barrioId] = [arista]

    def obtenerAristas(self, barrio):
        return self.red.get(barrio, [])

    def dijkstra(self, start: str):
        print(self.red)
        # Inicializar estructuras
        distances = {nodo: float('inf') for nodo in self.red}
        distances[start] = 0
        previous_nodes = {nodo: None for nodo in self.red}
        visited = set()
        heap = [(0, start)]  # (distancia, nodo)

        # Algoritmo principal
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_node in visited:
                continue
            visited.add(current_node)

            for arista in self.red[current_node]:  # Iterar sobre las aristas
                neighbor = arista["nodoId"]
                distance = current_distance + arista["flujo"]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = (current_node, arista)
                    heapq.heappush(heap, (distance, neighbor))

        return distances, previous_nodes  # Retornar diccionarios

    def shortestPathsFromTanks(self):
        tank_nodes = [nodo for nodo in self.red if any(arista["tankId"] == nodo for arista in self.red[nodo])]
        if not tank_nodes:
            print("No se encontraron tanques.")
            return Red()  # Retornar un barrio vacío si no hay tanques

        distances_from_tanks = {tank: {} for tank in tank_nodes}
        paths_from_tanks = {tank: {} for tank in tank_nodes}

        for tank in tank_nodes:
            print(f"Ejecutando Dijkstra desde el tanque: {tank}")
            distances, previous_nodes = self.dijkstra(tank)
            distances_from_tanks[tank] = distances
            paths_from_tanks[tank] = previous_nodes

        # Asignación de nodos a tanques
        nodo_a_tanque = {}
        for nodo in self.red:
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
                    subgrafo.agregarArista(previous_node, AristaBarrio(**arista))
                    current_id = previous_node
                else:
                    print(f"Error: Expected tuple, but got {paths_from_tanks[tank_id][current_id]}")
                    break
        print(subgrafo.toDict())
        return subgrafo
    def menorFlujo(self):
        menorFlujo = float('inf')
        for nodo in self.barrio:
            for arista in self.barrio[nodo]:
                if arista["flujo"] < menorFlujo:
                    menorFlujo = arista["flujo"]
        return menorFlujo
    
    def optimizar(self):
        grafoOptimo = self.shortestPathsFromTanks()
        menorFlujo = self.menorFlujo()
        for nodo in grafoOptimo.barrio:
            print(grafoOptimo.barrio)
            for arista in grafoOptimo.barrio[nodo]:
                print(arista)
                arista.flujoOptimo = menorFlujo
        return grafoOptimo

    def __repr__(self):
        return f'Red({self.red})'

    def toJson(self):
        return json.dumps(self.toDict())

    @classmethod
    def fromJson(self, json_str):
        data = json.loads(json_str)
        self.fromDict(data)

    def toDict(self):
        return {
            'barrios': {barrio: [arista.toDict() for arista in aristas] for barrio, aristas in self.red.items()}
        }

    @classmethod
    def fromDict(self, data):
        self.red = {}
        for barrio, aristas in data['barrios'].items():
            self.red[barrio] = [AristaBarrio.fromDict(arista) for arista in aristas]

    def optimizarRed(self):
        pass