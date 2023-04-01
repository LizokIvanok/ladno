#Создай собственный Шутер!

from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, coord_x, coord_y, player_speed, width, height, player_image):
        sprite.Sprite.__init__(self)
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #self.rect.x += randint(-30,30)
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(30, 770)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 20, 15, 'bullet.png')
        bullets.add(bullet)

lost = 0
kills = 0
lifes = 3

font.init()
font1 = font.SysFont('Times New Roman', 36)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(randint(30,670), 0, randint(5,10), 80, 50, 'pablo.png')
    monsters.add(monster)
   
bullets = sprite.Group()

window = display.set_mode((700,500))
display.set_caption('Кароч Пабло топ')
background = transform.scale(image.load('background.jpg'), (700,500))

ship = Player(315,400,10,80,100,'shelly.png')

clock = time.Clock()
game = True
while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                ship.shoot()
    
    window.blit(background, (0,0))
    ship.reset()
    ship.move()

    ship.update()
    monsters.update()
    bullets.update()

    monsters.draw(window)
    bullets.draw(window)

    text_lost = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
    window.blit(text_lost, (10,90))

    text_kills = font1.render('Сбито:' + str(kills), 1, (255,255,255))
    window.blit(text_kills, (10,50))

    if sprite.spritecollide(ship, monsters, True): 
        lifes -= 1

    if lifes == 0:
        game = False

    collides = sprite.groupcollide(monsters, bullets,True,True)
    for c in collides:
        kills += 1
        monster = Enemy(randint(30,770), 0,randint(5,10), 80, 50, 'spike.png')
        monsters.add(monster)

    display.update()
    time.delay(50)