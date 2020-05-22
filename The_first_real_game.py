import pygame as py
import random
import os
import neat


picture_path = 'C:/Users/shttu/source/repos/The first real game/The first real game/picture'

Green = (0,255,0)
Red = (255,0,0)
Blue = (0,0,255)
White = (255,255,255)
Black = (0,0,0)

Border_x = 1000
Border_y = 600

py.init()
Win = py.display.set_mode((Border_x,Border_y))
py.display.set_caption("Escaping!")
whole = True


while whole:
    #..............................................
    All_sprites = py.sprite.Group()
    class Player(py.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.pictures = [py.image.load("C:/Users/shttu/source/repos/The first real game/The first real game/picture/player_front1.png").convert_alpha(), py.image.load("C:/Users/shttu/source/repos/The first real game/The first real game/picture/player_front2.png").convert_alpha(),py.image.load("C:/Users/shttu/source/repos/The first real game/The first real game/picture/player_back1.png").convert_alpha(),py.image.load("C:/Users/shttu/source/repos/The first real game/The first real game/picture/player_back2.png").convert_alpha()]
            self.image = self.pictures[0]
            self.rect = self.image.get_rect()
            self.rect.x += 250
            self.rect.y = Border_y//2- self.rect.height//2 + 150
            self.acceler = -10 #acceleration for jump
            self.jump = False
            self.prev_tick = py.time.get_ticks()/1000 #set a time variable for controlling the jump move, convert it into second
            self.countframe = 0

        def update(self):
            self.countframe += 1
            now = py.time.get_ticks()/1000 #convert it into second
            if py.key.get_pressed()[py.K_d]:
                self.rect.x+=1
                if (self.image == self.pictures[0] or self.image == self.pictures[2]) and self.countframe > 10:
                    self.countframe = 0
                    self.image = self.pictures[1]
                elif (self.image == self.pictures[1] or self.image == self.pictures[3]) and self.countframe > 10:
                    self.countframe = 0
                    self.image = self.pictures[0]

            if py.key.get_pressed()[py.K_a]:
                self.rect.x-=1
                if (self.image == self.pictures[0] or self.image == self.pictures[2]) and self.countframe > 10:
                    self.countframe = 0
                    self.image = self.pictures[3]
                elif (self.image == self.pictures[1] or self.image == self.pictures[3]) and self.countframe > 10:
                    self.countframe = 0
                    self.image = self.pictures[2]

            if py.key.get_pressed()[py.K_SPACE] or py.key.get_pressed()[py.K_w]:
                self.jump = True
            if self.jump and (now - self.prev_tick)>=0.05: #if it is jumping and there is 0.5 second pass from last frame
                self.prev_tick = now
                Dropping = 1 #since acceler power of 2 will always gives positive value, we need it to incre y when it is dropping
                if self.acceler > 0:
                    Dropping = -1
                self.rect.y -= self.acceler**2 //2 * Dropping #quadratic func to make it a nice jumping curve
                self.acceler += 1
                self.rect.x += 3
                if self.acceler > 10:
                    self.acceler = -10
                    self.jump = False
                if self.rect.y < 0:
                    self.rect.y = 0
                if self.rect.x < 0:
                    self.rect.x = 0
                if self.rect.right > Border_x:
                    self.rect.x = Border_x - self.rect.width

    class trap(py.sprite.Sprite):
        def __init__(self, distance):
            super().__init__()
            self.image = py.image.load(os.path.join(picture_path,"obstacle.png"))
            self.rect = self.image.get_rect()
            self.rect.x = Border_x + 10 + distance*500
            self.rect.y = random.randint(Border_y//2+100,Border_y//2+300)


        def update(self):
            self.rect.x -= 1 #moving to the left 
            self.rect.y -= random.randint(-3,3)
            if self.rect.right < 0:
                self.rect.x = Border_x + 10
                self.rect.y = random.randint(Border_y//2+100,Border_y//2+200)

    class Ground(py.sprite.Sprite):
        def __init__(self,index):
            super().__init__()
            image = py.image.load(os.path.join(picture_path,"background.png"))
            self.image = py.transform.scale(image,(1000,200))
            self.rect = self.image.get_rect()
            self.rect.y = 370
            self.rect.x = index*1000 
            #make 2 ground, if it is the first one, it start at 0 (index =0), if it is the second one(index = 1), it starts at the position after the first one 

        def update(self):
            self.rect.x -= 1
            if self.rect.right < 0:
                self.rect.x = Border_x-1

    for i in range(2):
        ground = Ground(i)
        All_sprites.add(ground)
    player = Player()
    All_sprites.add(player)
    TrapSprites = py.sprite.Group()
    for i in range(2):
        Tree1 = trap(i)
        All_sprites.add(Tree1)
        TrapSprites.add(Tree1)

    
    #...............above for running game.......below for before game start
    class startgame(py.sprite.Sprite):
        def __init__(self):
            super().__init__()
            text_startgame = py.font.SysFont("Times New Roman, Arial", 50,True)
            text = text_startgame.render("Start Game",True,Black)
            self.image = text
            self.rect = self.image.get_rect()
            self.rect.x = Border_x//2 - self.rect.width//2
            self.rect.y = 300

    class startgameTitle(py.sprite.Sprite):
        def __init__(self):
            super().__init__()
            Game_title = py.font.SysFont("Times New Roman, Arial", 150, True)
            text = Game_title.render("Escaping !", True, Black)
            self.image = text
            self.rect = self.image.get_rect()
            self.rect.x = Border_x//2-self.rect.width//2
            self.rect.y = 100

    before_game_sprite = py.sprite.Group()
    Startgame = startgame()
    StartgameTitle = startgameTitle()
    before_game_sprite.add(Startgame)
    before_game_sprite.add(StartgameTitle)

    #.....................below for Game over
    class Gameover(py.sprite.Sprite):
        def __init__(self):
            super().__init__()
            Text_middle = py.font.Font(py.font.get_default_font(),100)
            text = Text_middle.render("Game Over",True,Black)
            self.image = text
            self.rect = self.image.get_rect()
            self.rect.x = Border_x//2-self.rect.width//2
            self.rect.y = Border_y//2-self.rect.height//2 - 50
    class GameRestart(py.sprite.Sprite):
        def __init__(self):
            super().__init__()
            Text_lower = py.font.Font(py.font.get_default_font(),50)
            text = Text_lower.render("Restart?",True,Black)
            self.image = text
            self.rect = self.image.get_rect()
            self.rect.x = Border_x//2-self.rect.width//2
            self.rect.y = Border_y//2-self.rect.height//2 + 100
    gamerestart = GameRestart()
    gameover = Gameover()
    after_game_sprite = py.sprite.Group()
    after_game_sprite.add(gameover)
    after_game_sprite.add(gamerestart)

    #.....................below for creating a mouse sprite
    class mouse(py.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect = py.Rect(0,0,1,1)

        def update(self):
            mx,my = py.mouse.get_pos()
            self.rect.x = mx
            self.rect.y = my

    Mouse = mouse()

    #...............................................................
    #.....................Starting the Game........................
    Game_over = False
    Running = True
    Start_game = False
    while Running:
        for event in py.event.get():
            if event.type == py.QUIT or py.key.get_pressed()[py.K_ESCAPE]:
                Running = False
                whole = False
                Game_over = False
    
        #drawing section
        Win.fill(White)
        if Start_game:
            All_sprites.update()
        All_sprites.draw(Win)
        cover_ground = py.Surface((1000,300))
        cover_ground.fill(White)
        Win.blit(cover_ground,(0,530))


        if not Start_game:
            before_game_sprite.draw(Win)

        if py.mouse.get_pressed()[0]: 
            Mouse.update()
            if py.sprite.collide_rect(Mouse,Startgame):
                Start_game = True
        for i in TrapSprites:
            if py.sprite.collide_mask(player,i):
                Game_over = True
                Running = False

        py.display.update()
        py.time.wait(5)

    while Game_over:
        Win.fill(White)
        after_game_sprite.draw(Win)
        py.display.update()
        if py.mouse.get_pressed()[0]: 
            Mouse.update()
            if py.sprite.collide_rect(Mouse,gamerestart):
                Game_over = False
                Running = False
            if py.sprite.collide_rect(Mouse,gameover):
                Game_over = False
                whole = False

        for event in py.event.get():
            if event.type == py.QUIT or py.key.get_pressed()[py.K_ESCAPE]:
                Game_over = False
                whole = False
       
py.quit()
  
