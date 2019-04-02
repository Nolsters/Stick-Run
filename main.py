import pygame
import random

pygame.init()
WIDTH = 1920
HEIGHT = 1080
win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

pygame.display.set_caption("Super Mad Man")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png')]
char = pygame.image.load('Facing.png')
crouch = pygame.image.load('Crouch.png')
bg = pygame.image.load('BG.jpg')
bg2 = pygame.image.load('start.png')
bg3 = pygame.image.load('bg3.jpg')
hitbox = pygame.image.load('hitbox.png')
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
black = (0,0,0)
RED = (255, 0, 0)
myfont = pygame.font.SysFont("comicsans", 45)



clock = pygame.time.Clock()

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.left = False
        self.right = False
        self.isDuck = False
        self.walkCount = 0
        self.jumpCount = 10
        self.duckCount = 10
        self.health = 100
        self.image = hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    def draw(self, win):
        if self.walkCount + 1 >= 10:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.isDuck:
            win.blit(crouch, (self.x, self.y))
        else:
            win.blit(char, (self.x, self.y))


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


def redrawGameWindow():
    man.draw(win)
    pygame.display.update()


# mainloop
man = player(200, 410, 64, 64)

score = 0
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = pygame.sprite.Group()
rungame = False

for i in range(28):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
all_sprites.add(man)
player.add(man)

def game_menu():
    run2 = True
    while run2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
        win.blit(bg2, (900, 550))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_end()
        pygame.display.update()

def play_game():
    rungame = True
    score = 0
    while rungame:
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and man.x > man.vel:
            if man.isDuck:
                man.x -= man.vel - 5
                man.rect.x -= man.vel -5
                man.left = True
                man.right = False
            else:
                man.x -= man.vel
                man.rect.x -= man.vel
                man.left = True
                man.right = False
        elif keys[pygame.K_RIGHT] and man.x < 1920 - man.width - man.vel:
            if man.isDuck:
                man.x += man.vel - 5
                man.rect.x += man.vel - 5
                man.right = True
                man.left = False
            else:
                man.x += man.vel
                man.rect.x += man.vel
                man.right = True
                man.left = False
        if not (man.isDuck):
            if keys[pygame.K_DOWN]:
                man.isDuck = True
            else:
                man.isDuck = False
        else:
            man.right = False
            man.left = False
            man.walkCount = 0

        if not (man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.right = False
                man.left = False
                man.isDuck = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                (man.jumpCount ** 2) * 0.5 * neg
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.rect.y = man.y
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
        if pygame.sprite.groupcollide(player, mobs, 0, 1):
            man.health -= 20
        win.blit(bg, (0, 0))
        all_sprites.update()
        all_sprites.draw(win)
        health = man.health
        scoretext = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
        life = myfont.render("Life {0}".format(health), 1, (0,0,0))
        win.blit(scoretext, (5, 10))
        win.blit(life, (10, 100))
        score += 1
        redrawGameWindow()
        if man.health <= 0:
            return score
    return score

def game_highscores():
    run2 = True
    while run2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
        win.blit(bg3, (0, 0))
        pygame.display.update()


def game_end():
    run = True
    score = play_game()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        final_score = myfont.render("You Scored {0}".format(score), 1, (0, 0, 0))
        navigate = myfont.render("press H for highscores!", 1, (0,0,0))
        win.blit(bg, (0, 0))
        win.blit(final_score, (900, 400))
        win.blit(navigate, (900, 550))
        redrawGameWindow()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            game_highscores()




game_menu()


pygame.quit()