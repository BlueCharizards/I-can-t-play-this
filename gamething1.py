import pygame
import random
from os import path

WIDTH = 600 #width of our game window
HEIGHT = 480 #height of our game window
FPS = 60

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (115, 0, 195)
PINK = (205, 0, 102)
light_blue = (65, 105, 255)

pygame.init()
pygame.mixer.init() #initializes sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #create screen
pygame.display.set_caption("Game") #give game a name
clock = pygame.time.Clock() #keep track of speed/time

img_dir = path.join(path.dirname(__file__),"Game")
player_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "enemyBlack3.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "star_silver.png")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (30,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom =(HEIGHT-10)
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4,10)
        self.speedx = random.randrange(-10,10)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left <0 or self.rect.right > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4,15)
            self.speedx = random.randrange(-10, 10)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#Initialize and create game window
        

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
for i in range(15):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
bullets = pygame.sprite.Group()

#Game Loop
running = True
while running:
    clock.tick(FPS) #keep the loop running at the right speed
    #Process Inputs (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        
    #Updates
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    #Renders (draws)
    screen.fill(PURPLE)
    all_sprites.draw(screen)
    #after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()

