import pygame
import sys
from menuVar import ResponsiveMenu
from grafo import parse_grafo, draw_grafo


def main():
    pygame.init()
    width, height = 800, 500
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Gestión de Redes")

    logo = pygame.image.load('logo.jpg').convert_alpha()
    logo = pygame.transform.scale(logo, (width, height))
    logo.set_alpha(40)

    menu_options = ["Gestión de la Red", "Simulaciones", "Optimización", "Mantenimiento", "Visualización", "Salir"]
    menu = ResponsiveMenu(screen, menu_options)

    nodos, aristas = parse_grafo(r"C:\Users\Usuario\Documents\Proyectos Estructura de Datos\Project2\project2-data-struct\front\datos.json")


    offset = [0, 0]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                logo = pygame.transform.scale(logo, (width, height))
                menu.calculate_layout()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    offset[1] -= 20
                elif event.button == 5:  # Scroll down
                    offset[1] += 20
                elif event.button == 1:  # Left click
                    menu.handle_event(event)

        screen.fill((255, 255, 255))
        screen.blit(logo, (0, 0))
        draw_grafo(screen, nodos, aristas, offset)
        menu.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
