import pygame as pg
from front.ViewRed import ViewRed

class Principal:
    def __init__(self):
        self.estado = "menu"
        pg.init()
        self.screen = pg.display.set_mode((1000, 600))
        pg.display.set_caption("Menu")
        self.font = pg.font.Font(None, 40)
        self.menu()

    def dibujar_texto(self, texto, pos):
        texto_surface = self.font.render(texto, True, (0, 0, 0))  # Texto en color negro
        self.screen.blit(texto_surface, pos)

    def menu(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if self.visualizar_red_btn.collidepoint(mouse_pos):
                        view_red = ViewRed("datos.json")
                        view_red.correr()
                    elif self.visualizar_barrio_btn.collidepoint(mouse_pos):
                        print("Visualizar Barrio")
                    elif self.agregar_nodo_btn.collidepoint(mouse_pos):
                        print("Agregar Nodo")
                    elif self.crear_barrio_btn.collidepoint(mouse_pos):
                        print("Crear Barrio")

            self.screen.fill((255, 255, 255))  # Fondo blanco

<<<<<<< HEAD
    nodos, aristas = parse_grafo(r"./front/datos.json", "A")
=======
            # Dibujar botones con cajas alrededor
            self.visualizar_red_btn = pg.draw.rect(self.screen, (0, 0, 255), (100, 100, 300, 50))
            self.visualizar_red_box = pg.draw.rect(self.screen, (0, 0, 0), (95, 95, 310, 60), 3)
            self.visualizar_barrio_btn = pg.draw.rect(self.screen, (0, 0, 255), (100, 200, 300, 50))
            self.visualizar_barrio_box = pg.draw.rect(self.screen, (0, 0, 0), (95, 195, 310, 60), 3)
            self.agregar_nodo_btn = pg.draw.rect(self.screen, (0, 0, 255), (100, 300, 300, 50))
            self.agregar_nodo_box = pg.draw.rect(self.screen, (0, 0, 0), (95, 295, 310, 60), 3)
            self.crear_barrio_btn = pg.draw.rect(self.screen, (0, 0, 255), (100, 400, 300, 50))
            self.crear_barrio_box = pg.draw.rect(self.screen, (0, 0, 0), (95, 395, 310, 60), 3)
>>>>>>> 053c822 (front maybe is ok)

            # Dibujar texto de botones
            self.dibujar_texto("Visualizar Red", (110, 110))
            self.dibujar_texto("Visualizar Barrio", (110, 210))
            self.dibujar_texto("Agregar Nodo", (110, 310))
            self.dibujar_texto("Crear Barrio", (110, 410))

            pg.display.flip()

        pg.quit()

# Ejecutar la aplicación
if __name__ == "__main__":
    Principal()
