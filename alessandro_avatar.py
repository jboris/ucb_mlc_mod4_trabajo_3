from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import threading

from pygame.locals import *

from alessandro import AlessandroBot


class AlessandroAvatarApp:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((300, 400))
        pygame.display.set_caption("Alessandro Avatar")
        self.closed_mouth_image = pygame.image.load("img/avatar0.png").convert_alpha()
        self.open_mouth_image = pygame.image.load("img/avatar1.png").convert_alpha()
        self.thinking_image = pygame.image.load("img/avatar2.png").convert_alpha()
        self.current_image = None        
        self.ale_bot = AlessandroBot()
        self.active_animation = False
        self.thread_sound = None
        self.button = pygame.Rect(100, 300, 100, 50)
        self.button_color_normal = (0, 128, 255)
        self.button_color = self.button_color_normal
        self.button_color_click = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 26)
        self.button_click_tiempo = 500
        self.thinking = False

    def run(self):
        self.show_avatar()

    def show_avatar(self):
        self.current_image = self.closed_mouth_image
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.button.collidepoint(event.pos):
                        self.button_color = self.button_color_click
                        pygame.time.set_timer(USEREVENT, self.button_click_tiempo)
                        self.thread_sound = threading.Thread(target=self.play_sound)
                        self.thread_sound.start()
                elif event.type == USEREVENT:
                    self.button_color = self.button_color_normal
            window_width, window_height = self.window.get_size()
            image_width, image_height = self.current_image.get_size()
            x = (window_width - image_width) // 2
            y = 0
            self.window.blit(self.current_image, (x, y))
            pygame.draw.rect(self.window, self.button_color, self.button)
            text = self.font.render("Preguntar", True, self.text_color)
            text_rect = text.get_rect(center=self.button.center)
            self.window.blit(text, text_rect)
            pygame.display.flip()
            if self.active_animation:
                pygame.time.delay(200)
                self.change_imagen()
            else:
                if self.thinking:
                    self.current_image = self.thinking_image
                else:
                    self.current_image = self.closed_mouth_image
            clock.tick(30)
        pygame.quit()

    def change_imagen(self):
        if self.current_image == self.closed_mouth_image:
            self.current_image = self.open_mouth_image
        else:
            self.current_image = self.closed_mouth_image
            
    def play_sound(self, verbose=False):
        def synthesis_started_callback(evt):
            pygame.time.delay(2000)
            self.active_animation = True
            self.thinking = False
            
        def synthesis_complete_callback(evt):
            self.active_animation = False

        def thinking_callback():
            self.thinking = True
            self.active_animation = False
            
        self.ale_bot.ask(verbose, synthesis_started_callback, synthesis_complete_callback, thinking_callback)

if __name__ == "__main__":
    app = AlessandroAvatarApp()
    app.run()
