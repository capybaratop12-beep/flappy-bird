import pygame
import os
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('flappy bird')

font = pygame.font.SysFont('Bauhaus 93',60)
white = (255,255,255)

def loadIMG(path):
    current_dir = os.path.dirname(__file__)
    img_path = os.path.join(current_dir, path)
    print(img_path)
    return pygame.image.load(img_path)

def file_path(path):
    current_dir = os.path.dirname(__file__)
    return  os.path.join(current_dir, path)

bg = loadIMG(r'img\bg.png')
ground_img = loadIMG(r'img\ground.png')

ground_scroll = 0
scroll_speed = 2
flying = False
game_over = False
pipe_gap = 300
pipe_fr = 1500
last_pipe = pygame.time.get_ticks()
pass_pipe = False
score = 0

def draw_text(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = loadIMG(rf'img\bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = - 10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index],self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadIMG(r'img\pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - pipe_gap // 2]
        if position == -1:
            self.rect.topleft = [x,y + pipe_gap // 2]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100,screen_height // 2)
bird_group.add(flappy)


run = True
while run:

    clock.tick(fps)

    screen.blit(bg,(0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)


    screen.blit(ground_img, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if  bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score),font,white,screen_width // 2,20)

    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_fr:
            pipe_height = random.randint(-100,100)
            pipe_down = Pipe(screen_width, screen_height // 2 + pipe_height, -1)
            pipe_up = Pipe(screen_width, screen_height // 2 + pipe_height, 1)
            pipe_group.add(pipe_down)
            pipe_group.add(pipe_up)
            last_pipe = time_now
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == True and flying == False:
                ground_scroll = 0
                scroll_speed = 2
                flying = False
                game_over = False
                last_pipe = pygame.time.get_ticks()
                pass_pipe = False
                score = 0
                bird_group = pygame.sprite.Group()
                pipe_group = pygame.sprite.Group()

                flappy = Bird(100, screen_height // 2)
                bird_group.add(flappy)

    pygame.display.update()

pygame.quit()