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

    def redOptima(self):
        # Crear una lista de todas las aristas
        aristas = []
        for barrio, conexiones in self.red.items():
            for arista in conexiones:
                aristas.append((arista["flujo"], barrio, arista["barrioId"]))

        # Ordenar las aristas por flujo
        aristas.sort()

        # Inicializar estructuras para el algoritmo de Kruskal
        parent = {}
        rank = {}

        def find(nodo):
            if parent[nodo] != nodo:
                parent[nodo] = find(parent[nodo])
            return parent[nodo]

        def union(nodo1, nodo2):
            root1 = find(nodo1)
            root2 = find(nodo2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]:
                    rank[root2] += 1

        # Inicializar los conjuntos disjuntos
        for barrio in self.red:
            parent[barrio] = barrio
            rank[barrio] = 0

        # Algoritmo de Kruskal para encontrar el árbol de expansión mínima
        mst = []
        for flujo, barrio1, barrio2 in aristas:
            if find(barrio1) != find(barrio2):
                union(barrio1, barrio2)
            mst.append((barrio1, barrio2, flujo))

        # Crear la nueva red óptima
        red_optima = Red()
        for barrio in self.red:
            red_optima.agregarBarrio(barrio)
        for barrio1, barrio2, flujo in mst:
            arista = next(arista for arista in self.red[barrio1] if arista["barrioId"] == barrio2)
            red_optima.agregarArista(barrio1, arista)

        return red_optima

    def menorFlujo(self):
        menorFlujo = float('inf')
        for barrio in self.red:
            for arista in self.red[barrio]:
                if arista["flujo"] < menorFlujo:
                    menorFlujo = arista["flujo"]
        return menorFlujo
    
    def optimizar(self):
        grafoOptimo = self.redOptima()
        menorFlujo = grafoOptimo.menorFlujo()
        for nodo in grafoOptimo.red:
            for arista in grafoOptimo.red[nodo]:
                arista["flujoOptimo"] = menorFlujo
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
            'barrios': {barrio: [arista for arista in aristas] for barrio, aristas in self.red.items()}
        }

    @classmethod
    def fromDict(self, data):
        self.red = {}
        for barrio, aristas in data.items():
            self.red[barrio] = [AristaBarrio.fromDict(arista) for arista in aristas]

    def optimizarRed(self):
        pass