import pygame
import json
import math

class ViewRed:
    def __init__(self):
        pygame.init()
        self.estado = "Visualizar Red"
        self.window_size = (1200, 800)  # Tamaño ajustado para manejar más nodos y barrios
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Visualización de Red de Nodos y Barrios")

        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.NODE_COLOR = (0, 0, 255)
        self.TANK_COLOR = (255, 0, 0)
        self.EDGE_COLOR = (0, 255, 0)
        self.OBSTRUCTED_EDGE_COLOR = (255, 0, 0)

        # Cargar datos desde el archivo JSON
        with open('datos.json', 'r') as f:
            self.data = json.load(f)

        # Generar posiciones y conexiones
        self.node_positions = self.generate_grid_layout()
        self.edges = self.create_edges()
        self.optimal_edges = self.create_optimal_edges()

    def generate_grid_layout(self):
        """
        Genera posiciones de nodos distribuidos en una cuadrícula.
        """
        positions = {}
        num_nodes = len(self.data['nodos'])
        grid_size = math.ceil(math.sqrt(num_nodes))
        padding = 50
        cell_width = (self.window_size[0] - 2 * padding) // grid_size
        cell_height = (self.window_size[1] - 2 * padding) // grid_size

        for index, node in enumerate(self.data['nodos'].keys()):
            row = index // grid_size
            col = index % grid_size
            x = padding + col * cell_width + cell_width // 2
            y = padding + row * cell_height + cell_height // 2
            positions[node] = (x, y)

        return positions

    def create_edges(self):
        """
        Crea una lista de aristas regulares desde la estructura de barrios.
        """
        edges = []
        for barrio, conexiones in self.data['barrios'].items():
            for origen, destinos in conexiones.items():
                for destino in destinos:
                    flujo = destino['flujo']
                    obstruido = destino['obstruido']
                    nodo_destino = destino['nodoId']
                    edges.append((origen, nodo_destino, flujo, obstruido))
        return edges

    def create_optimal_edges(self):
        """
        Crea aristas basadas en la estructura de barrios óptimos.
        """
        optimal_edges = []
        for barrio, conexiones in self.data['barriosOptimos'].items():
            for origen, destinos in conexiones.items():
                for destino in destinos:
                    flujo = destino['flujo']
                    obstruido = destino['obstruido']
                    nodo_destino = destino['nodoId']
                    optimal_edges.append((origen, nodo_destino, flujo, obstruido))
        return optimal_edges

    def viewRed(self):
        """
        Visualiza la red de nodos y aristas.
        """
        self.screen.fill(self.WHITE)

        # Dibujar aristas regulares
        for edge in self.edges:
            origen, destino, flujo, obstruido = edge
            if origen in self.node_positions and destino in self.node_positions:
                color = self.OBSTRUCTED_EDGE_COLOR if obstruido else self.EDGE_COLOR
                pygame.draw.line(self.screen, color, self.node_positions[origen], self.node_positions[destino], 2)
                x_medio = (self.node_positions[origen][0] + self.node_positions[destino][0]) // 2
                y_medio = (self.node_positions[origen][1] + self.node_positions[destino][1]) // 2
                font = pygame.font.Font(None, 24)
                flujo_text = font.render(f"{flujo:.1f}", True, self.BLACK)
                self.screen.blit(flujo_text, (x_medio, y_medio))

        # Dibujar nodos
        for node, pos in self.node_positions.items():
            tank = self.data['nodos'][node].get('tank')
            color = self.TANK_COLOR if tank else self.NODE_COLOR
            pygame.draw.circle(self.screen, color, pos, 20)
            font = pygame.font.Font(None, 36)
            text = font.render(node, True, self.WHITE)
            self.screen.blit(text, (pos[0] - 10, pos[1] - 10))

        pygame.display.flip()

    def run(self):
        """
        Ejecuta el loop principal.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.viewRed()

        pygame.quit()


# Ejecutar visualización
if __name__ == "__main__":
    visualizer = ViewRed()
    visualizer.run()
