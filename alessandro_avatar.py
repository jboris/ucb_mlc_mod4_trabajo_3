from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import threading

from pygame.locals import *

from alessandro import AlessandroBot


class AlessandroAvatarApp:
    def __init__(self):
        pygame.init()

        self.ventana = pygame.display.set_mode((300, 400))
        pygame.display.set_caption("Alessandro Avatar")

        self.imagen_boca_cerrada = pygame.image.load("avatar0.png").convert_alpha()
        self.imagen_boca_abierta = pygame.image.load("avatar1.png").convert_alpha()

        self.current_image = None
        
        self.ale_bot = AlessandroBot()

        self.animacion_activa = False
        self.thread_sonido = None
        
        self.boton_rect = pygame.Rect(100, 300, 100, 50)
        self.boton_color_normal = (0, 128, 255)  # Color azul
        self.boton_color = self.boton_color_normal
        self.boton_color_clic = (255, 0, 0)  # Color rojo cuando se hace clic
        self.texto_color = (255, 255, 255)  # Color blanco
        self.font = pygame.font.Font(None, 26)
        self.boton_clic_tiempo = 500  # Tiempo en milisegundos (1 segundo)


    def run(self):
        self.mostrar_avatar()

    def mostrar_avatar(self):
        self.current_image = self.imagen_boca_cerrada
        clock = pygame.time.Clock()

        # Iniciar el hilo para reproducir el sonido
        #pygame.mixer.init()
        #thread_sonido = pygame.mixer.Sound("temp.wav")
        #thread_sonido.play()

        #thread_sonido = threading.Thread(target=self.reproducir_sonido)
        #thread_sonido.start()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.boton_rect.collidepoint(event.pos):
                        self.boton_color = self.boton_color_clic
                        pygame.time.set_timer(USEREVENT, self.boton_clic_tiempo)
                        self.thread_sonido = threading.Thread(target=self.reproducir_sonido)
                        self.thread_sonido.start()
                elif event.type == USEREVENT:
                    self.boton_color = self.boton_color_normal

            ventana_ancho, ventana_alto = self.ventana.get_size()

        # Obtener las dimensiones de la imagen actual
            imagen_ancho, imagen_alto = self.current_image.get_size()

        # Calcular las coordenadas para centrar la imagen horizontalmente
            x = (ventana_ancho - imagen_ancho) // 2
            y = 0

            self.ventana.blit(self.current_image, (x, y))
#            self.ventana.blit(self.current_image, (0, 0))

            pygame.draw.rect(self.ventana, self.boton_color, self.boton_rect)
            
            # Renderizar el texto en el botón
            texto = self.font.render("Preguntar", True, self.texto_color)
            texto_rect = texto.get_rect(center=self.boton_rect.center)
            self.ventana.blit(texto, texto_rect)

            pygame.display.flip()

            # Cambiar la imagen del avatar después de un tiempo para simular que la boca se abre
            if self.animacion_activa:
                pygame.time.delay(200)
                self.cambiar_imagen()
            else:
                self.current_image = self.imagen_boca_cerrada

            clock.tick(30)

        pygame.quit()

    def cambiar_imagen(self):
        if self.current_image == self.imagen_boca_cerrada:
            self.current_image = self.imagen_boca_abierta
        else:
            self.current_image = self.imagen_boca_cerrada
            
    def reproducir_sonido(self, verbose=False):
        def synthesis_started_callback(evt):
            pygame.time.delay(2000)
            self.animacion_activa = True
            
        def synthesis_complete_callback(evt):
            self.animacion_activa = False
            
        self.ale_bot.ask(verbose, synthesis_started_callback, synthesis_complete_callback)

if __name__ == "__main__":
    app = AlessandroAvatarApp()
    app.run()
