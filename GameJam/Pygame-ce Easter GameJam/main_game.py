import pygame, sys
from random import randint
from pygame.math import Vector2 as vector

class Game:
    def __init__(self):
        pygame.init()

        #settings
        self.game_width, self.game_height = 1280, 720

        self.circle_pos = vector(self.game_width // 2, self.game_height // 2)
        self.circle_radius = 69

        self.rect_pos = vector(self.circle_pos.x - 138, self.circle_pos.y + 100)

        #music
        self.bgm = pygame.mixer.Sound('bgm.mp3')

        #setting the screen
        self.screen = pygame.display.set_mode((self.game_width, self.game_height))
        pygame.display.set_caption('Atom tickler')

        #setting the clock
        self.clock = pygame.time.Clock()
        self.clock.tick(120)

        #circle agitation
        self.circle_agitation = 0

        #colors
        self.circle_color = ['#7a4d4a', '#f0a8a8', '#95dbda', '#4b34c5', '#21abd8']
        self.button_colors = ['#e690bc', '#aef6f7']
        self.screen_colors = ['#000080', '#9ae3b7']

        #font and text
        self.font = pygame.font.SysFont('Comic Sans MS', 69)
        self.ending_msg = self.font.render(':(', True, (255, 255, 255))
        self.ending_msg_rect = self.ending_msg.get_rect(center= (self.game_width // 2, self.game_height // 2))

        #playing music
        self.bgm.play(-1).set_volume(0.25)

        self.run()

    def agitate_circle(self):
        new_x = randint(-10, 10)
        new_y = randint(-10, 10)
        radius_size = randint(-30, 50)
        circle_random_color = self.circle_color[randint(0, len(self.circle_color) - 1)]
        if self.circle_agitation > 0:
            match self.circle_agitation:
                case 1:
                    pygame.draw.circle(self.screen, self.circle_color[4], (self.circle_pos.x + new_x * 2, (self.circle_pos.y - 100) + new_y), self.circle_radius)

                case 2:
                    pygame.draw.circle(self.screen, self.circle_color[4], (self.circle_pos.x + new_x * 3, (self.circle_pos.y - 100) + new_y * 3), self.circle_radius)
                case 3:
                    pygame.draw.circle(self.screen, self.circle_color[4], (self.circle_pos.x + (new_x * 8), (self.circle_pos.y - 100) + (new_y * 10)), self.circle_radius + radius_size)
                case 4:
                    pygame.draw.circle(self.screen, circle_random_color, (self.circle_pos.x + new_x * 25, (self.circle_pos.y - 100) + new_y * 15), self.circle_radius + radius_size)
                case 5:
                    reset = randint(0, 1)
                    if reset == 0:
                        self.circle_agitation += randint(-2, -1)
                    else:
                        self.circle_agitation += 1
                case 6:
                    pygame.draw.circle(self.screen, circle_random_color,
                                       (self.circle_pos.x + (new_x * 50), (self.circle_pos.y - 100) + (new_y * 30)),
                                       self.circle_radius + radius_size)
                    pygame.draw.circle(self.screen, circle_random_color,
                                       (self.circle_pos.x + (new_x * 50), (self.circle_pos.y - 100) + (new_y * 30)),
                                       self.circle_radius + radius_size)
                case 7:
                    pygame.draw.circle(self.screen, circle_random_color,
                                       (self.circle_pos.x + (new_x * 100), (self.circle_pos.y - 100) + (new_y * 50)),
                                       self.circle_radius + radius_size)
                    pygame.draw.circle(self.screen, circle_random_color,
                                       (self.circle_pos.x + (new_x * 100), (self.circle_pos.y - 100) + (new_y * 50)),
                                       self.circle_radius + radius_size)
                case 8:
                    self.fake_crash()
                case 9:
                    sys.exit()

    def draw(self):
        self.screen.fill(self.screen_colors[1])
        pygame.draw.circle(self.screen, self.circle_color[4], (self.circle_pos.x, self.circle_pos.y - 100), self.circle_radius)
        pygame.draw.rect(self.screen, self.button_colors[0], (self.rect_pos.x, self.rect_pos.y, 250 // 2, 100))
        pygame.draw.rect(self.screen, self.button_colors[1], (self.rect_pos.x + 150, self.rect_pos.y, 250 // 2, 100))


    def fake_crash(self):
        self.screen.fill(self.screen_colors[0])
        self.screen.blit(self.ending_msg, self.ending_msg_rect)
        self.bgm.stop()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.circle_agitation == 8:
                        self.circle_agitation += 1
                    if self.rect_pos.x <= mouse_pos[0] <= self.rect_pos.x + 125 and self.rect_pos.y <= mouse_pos[1] <= self.rect_pos.y + 100 and self.circle_agitation < 8:
                        self.circle_agitation += 1
                    if self.rect_pos.x + 150 <= mouse_pos[0] <= self.rect_pos.x + 275 and self.rect_pos.y <= mouse_pos[1] <= self.rect_pos.y + 100:
                        self.circle_agitation -= 1 if self.circle_agitation > 0 else 0

            #drawing elements
            self.draw()

            #checking if the circle is agitated
            self.agitate_circle()

            #updating screen
            pygame.display.update()

if __name__ == '__main__':
    Game().run()
