import pygame

pygame.init()

win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

pygame.display.set_caption("Super Mad Man")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png')]
char = pygame.image.load('Facing.png')
crouch = pygame.image.load('Crouch.png')
bg = pygame.image.load('BG.jpg')
bg2 = pygame.image.load('start.png')
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
black = (0,0,0)
myfont = pygame.font.SysFont("monospace", 16)



clock = pygame.time.Clock()

class player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 200, self.y, 29, 52)
        self.vel = 10
        self.isJump = False
        self.left = False
        self.right = False
        self.isDuck = False
        self.walkCount = 0
        self.jumpCount = 10
        self.duckCount = 10
        self.health = 100

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
        self.hitbox = (self.x + 17, self.y + 11, 164, 184)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)



def redrawGameWindow():
    man.draw(win)
    pygame.display.update()


# mainloop
man = player(200, 410, 64, 64)


score = 0
rungame = False

run = True
while run:
    clock.tick(35)
    rungame = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.blit(bg2, (200, 410))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        rungame = True
    while rungame:
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and man.x > man.vel:
            if man.isDuck:
                man.x -= man.vel - 5
                man.left = True
                man.right = False
            else:
                man.x -= man.vel
                man.left = True
                man.right = False
        elif keys[pygame.K_RIGHT] and man.x < 1920 - man.width - man.vel:
            if man.isDuck:
                man.x += man.vel - 5
                man.right = True
                man.left = False
            else:
                man.x += man.vel
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
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
        win.blit(bg, (0, 0))
        disclaimertext = myfont.render("Some disclaimer...", 1, (0,0,0))
        win.blit(disclaimertext, (5, 480))

        scoretext = myfont.render("Score {0}".format(score), 1, (0,0,0))
        win.blit(scoretext, (5, 10))
        score += 1
        redrawGameWindow()
pygame.quit()