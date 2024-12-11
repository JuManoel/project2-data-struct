import pygame
import json

def parse_grafo(filename):
    """
    Carga y convierte un archivo JSON en listas de nodos y aristas para visualizar el grafo.

    Args:
        filename (str): Ruta al archivo JSON.

    Returns:
        tuple: Diccionario con nodos y lista de aristas.
    """
    with open(filename, 'r') as f:
        data = json.load(f)

    nodos = {nodo_id: nodo_data for nodo_id, nodo_data in data["nodos"].items()}
    aristas = [
        (origen, arista["nodo"]["id"], arista["flujo"], bool(arista["obstruido"]))
        for origen, conexiones in data["barrios"]["A"].items()
        for arista in conexiones
    ]

    return nodos, aristas


def draw_grafo(screen, nodos, aristas, offset):
    """
    Dibuja el grafo en Pygame con posiciones personalizadas para los nodos.

    Args:
        screen (pygame.Surface): Pantalla donde se dibuja.
        nodos (dict): Nodos del grafo.
        aristas (list): Lista de aristas con sus datos.
    """
    # Define posiciones personalizadas para los nodos
    node_positions = {
        "A": (100, 100),
        "B": (200, 200),
        "C": (200, 50),
        "D": (300, 150),
        "E": (300, 250),
        "F": (400, 50),
        "G": (400, 200),
        "H": (500, 50),
        "I": (500, 250),
        "J": (600, 150)
    }

    # Ajustar posiciones con el offset
    for nodo in node_positions:
        x, y = node_positions[nodo]
        node_positions[nodo] = (x + offset[0], y + offset[1])

    # Dibujar aristas
    for origen, destino, flujo, obstruido in aristas:
        if origen in node_positions and destino in node_positions:
            start_pos = node_positions[origen]
            end_pos = node_positions[destino]
            color = (255, 0, 0) if obstruido else (0, 255, 0)
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

            # Dibujar flujo en el punto medio
            x_medio = (start_pos[0] + end_pos[0]) // 2
            y_medio = (start_pos[1] + end_pos[1]) // 2
            font = pygame.font.Font(None, 24)
            flujo_text = font.render(f"{flujo:.1f}", True, (0, 0, 0))
            screen.blit(flujo_text, (x_medio, y_medio))

    # Dibujar nodos
    for nodo, pos in node_positions.items():
        color = (0, 255, 0) if nodos[nodo]["tank"] else (0, 0, 255)
        pygame.draw.circle(screen, color, pos, 20)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(nodo, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Grafo Personalizado")

    # Cargar datos del grafo
    nodos, aristas = parse_grafo("grafo.json")  # Cambia a la ruta de tu archivo JSON
    offset = (0, 0)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_grafo(screen, nodos, aristas, offset)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
