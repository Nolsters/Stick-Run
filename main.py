import pygame   # Imports Pygame
import random   # Imports Random


'''
Pls Set width and height to 1920x1080 for the best resolution if this is not possible set it to your native resolution.
'''
pygame.init()
WIDTH = 750
HEIGHT = 550
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Sets window.

pygame.display.set_caption("Super Mad Man")  # Windows name


'''
Setting up global variables.
I use these for images when setting up the game.
In the future I would like to keep these in a separate document then import that document.
'''
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png')] # Walking Animation
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png')] # More Walking animmation
char = pygame.image.load('Facing.png')  # Facing you animation
crouch = pygame.image.load('Crouch.png')  # Crouching animation
bg = pygame.image.load('BG.jpg')  # Background 1
bg2 = pygame.image.load('start.png')  # Background 2 (Starting Background)
bg3 = pygame.image.load('bg3.jpg')  # Background image 3 (Not in use)
hitbox = pygame.image.load('hitbox.png') # Hit box image.
GREEN = (0, 128, 0)  # Green RGB
WHITE = (255, 255, 255)  # White RGB
black = (0,0,0)  # Black RGB
RED = (255, 0, 0)  # Red RBG
myfont = pygame.font.SysFont("comicsans", 45)  # Font Setup



clock = pygame.time.Clock()  # Setting up pygame time.



'''
Player class
This sets an x, y, width and height position.
We then set those values including rect positions as well.
Also an is jup lef right and is duck variable these track the users positions.
Then in the draw method we take in the win which is the window.
In the draw method it setups animations including switching from the 3 animations per motion and jumping and crouching
tracking. As well draw makes sure to draw player.
'''
class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)     # taking in the pygame.sprite class.
        self.x = x
        self.y = y             # Sets x y and width and height of player.
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.left = False       # Sets all positions to FALSE
        self.right = False
        self.isDuck = False
        self.walkCount = 0
        self.jumpCount = 10
        self.duckCount = 10
        self.health = 100   # Sets Health
        self.image = hitbox # Sets image to hitbox.
        self.rect = self.image.get_rect()   # Gets rect of the image.
        self.rect.x = x    # Sets x for rect
        self.rect.y = y    # Sets y for rect



    def draw(self, win):
        if self.walkCount + 1 >= 10:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))       # Runs through the 3 walk left animations.
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))      # Runs through the 3 walk right animations.\
            self.walkCount += 1
        elif self.isDuck:
            win.blit(crouch, (self.x, self.y))      # Displays crouch animation with the x and y position.
        else:
            win.blit(char, (self.x, self.y))        # Displays Standing animation with x and y pos.

'''
The mob class is the rain or red stuff falling.
It has much of the same code as the player the only diference is the speed and rect x and y positions.
The rect x and y are random and as well the speed is random from 1 to 8.
'''
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)    # taking in pygame.sprite class.
        self.image = pygame.Surface((30, 40))   # Sets image size.
        self.image.fill(RED)                   # Fills image red.
        self.rect = self.image.get_rect()       # Sets image to rect.
        self.rect.x = random.randrange(WIDTH - self.rect.width)     # Sets rect x and rect y.
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):      # Deals with the position of the rect or the image.
        self.rect.y += self.speedy  # Adds the speed to the rect y.
        if self.rect.top > HEIGHT + 10:     # If self.rect.top is greter than the height + 10 then updates image speeds.
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)






'''
Simple draw game function.
'''

def redrawGameWindow():
    man.draw(win)  # Draws Player.
    pygame.display.update()  # Updates display.


# Giving our player some details.
man = player(200, 410, 64, 64)

all_sprites = pygame.sprite.Group()  # Sets all_sprites to a group.
mobs = pygame.sprite.Group()  # Sets mobs to a group.
player = pygame.sprite.Group()  # Sets player to a grup.
rungame = False  # Sets rungame to False

for i in range(28):
    m = Mob()
    all_sprites.add(m)      # Creates and adds a mob to the list of mobs. (28)
    mobs.add(m)
all_sprites.add(man)    # Add man player to all sprites.
player.add(man)         # Adds man to player group.


'''
Game Menu.
Just the beginning allowing the user to start the game by clicking space.
'''
def game_menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.blit(bg2, (900, 550))   # Displays Background 2.
        keys = pygame.key.get_pressed()  # Sets keys.
        if keys[pygame.K_SPACE]:  # If user presses space
            game_end()  # Run game_end()
        pygame.display.update()  # Updates display.


'''
Main game loop.
This loop contains a lot of functions. It spawns all 
'''
def play_game():
    rungame = True  # Sets rungame to true
    score = 0   # Sets Score to 0
    man.health = 100    # Sets health to 100
    while rungame:  # Runs game loop
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
        keys = pygame.key.get_pressed()  # Sets the key variable to allow us to make key presses shorter later on.
        if keys[pygame.K_LEFT] and man.x > man.vel:  # On left click player will move left if there is room.
            if man.isDuck:  # Checks if player is duck.
                man.x -= man.vel - 5    # Moves character 5 units left.
                man.rect.x -= man.vel -5    # Moves rect 5 units left.
                man.left = True  # Sets man.left to true so animation will run.
                man.right = False  # Sets man.right to false.
            else:  # If player is not duck.
                man.x -= man.vel    # Player moves 10 left.
                man.rect.x -= man.vel   # Rect moves 10 left.
                man.left = True  # Sets left to True
                man.right = False   # Sets right to false
        elif keys[pygame.K_RIGHT] and man.x < 1920 - man.width - man.vel:    # The Code below is the same as above but for right.
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
            if keys[pygame.K_DOWN]:     # Checks if down key is pressed.
                man.isDuck = True       # Sets man is duck to True.
            else:
                man.isDuck = False      # Else set False
        else:
            man.right = False           # Sets all other variables False.
            man.left = False
            man.walkCount = 0

        if not (man.isJump):
            if keys[pygame.K_UP]:       # If up key is pressed.
                man.isJump = True       # Sets man is jump to True.
                man.right = False       # Sets other variables false.
                man.left = False
                man.isDuck = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1                            # Gravity caculations to make jumping realistic.
                (man.jumpCount ** 2) * 0.5 * neg
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.rect.y = man.y
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
        '''
        Using groupcollide it check if a player in the players class rect is overlapping with a mob in the mobs group
        the 0 and 1 stand for dokill. So the first 0 means it will not kill the player and the second indicates it will
        kill the mob.
        '''
        if pygame.sprite.groupcollide(player, mobs, 0, 1):
            man.health -= 20

        '''
        Updates Screen with score, life points, and all_sprites.
        '''
        win.blit(bg, (0, 0))
        all_sprites.update()
        all_sprites.draw(win)
        health = man.health
        scoretext = myfont.render("Score {0}".format(score), 1, (0, 0, 0))  # Sets up the current score.
        life = myfont.render("Life {0}".format(health), 1, (0,0,0))     # Sets up the current life score.
        win.blit(scoretext, (5, 10))    # Renders the score on screen.
        win.blit(life, (10, 100))   # Renders the life points.
        score += 1      # Adds 1 to the score.
        redrawGameWindow()  # Updates / redraws game window.
        if man.health <= 0:  # Checks if the players health is below or equal to 0
            return score    # Returns Score
    return score            # Returns Score



'''
Game End Function
This displays your score and the current highscore. And tells user to hit h to restart.

'''
def game_end():
    run = True  # Sets run to True
    score = play_game()  # Sets score to play_game() then runs play_game() to get the score.
    while run:  # Runs game loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        final_score = myfont.render("You Scored {0}".format(score), 1, (0, 0, 0))
        navigate = myfont.render("press space to start again! or  E to exit.", 1, (0,0,0))         # Sets up score and other text.
        win.blit(bg, (0, 0))     # Renders Background
        win.blit(final_score, (900, 400))   # Renders Final Score.
        win.blit(navigate, (900, 550))      # Renders navigate text.
        redrawGameWindow()                  # Updates window.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:    # On h press plays game again.
            play_game()    # Runs play_game()
        if keys[pygame.K_e]:
            pygame.quit()



#  Runs Game.
game_menu()

#  Quites game
pygame.quit()