#Створи власний Шутер!
from typing import Any
from pygame import *
from random import randint
mixer.init()
# mixer.music.load("space.ogg")
# mixer.music.play()
font.init()
font0 = font.Font(None,36)
fire_sound = mixer.Sound("fire.ogg")
bullets = sprite.Group()
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 30, -15)
        bullets.add(bullet)
        fire_sound.play()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost+1

    def respawn(self):
        self.rect.x = randint(80,win_width - 80)
        self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global score
        # Видалення пулі, якщо вона виходить за межі екрану
        if self.rect.y < 0:
            self.kill()
        # Видалення пулі та ворога, якщо вони зіткнулися
        elif sprite.spritecollide(self, monsters, True):
            self.kill()
            score = score+1
lost = 0
global score
score = 0

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80,win_width - 80),-40,80,50,randint(1,5))
    monsters.add(monster)
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
clock = time.Clock()



finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            ship.fire()

    if not finish:
        window.blit(background, (0,0))
        ship.update()
        ship.reset()

        text = font0.render('Рахунок:' + str(score), 1, (255,255,255))
        window.blit(text,(10,20))
        text_lose = font0.render('Пропущено:' + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        
        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        if len(monsters) == 0:
            # Затримка перед створенням нових ворогів
            for i in range(5):
                monster = Enemy('ufo.png',randint(80,win_width - 80),-40,80,50,randint(1,5))
                monsters.add(monster)

        if score >= 10:
            text_win = font0.render('U win!', 1, (255,255,255))
            window.blit(text_win, (win_width // 2 - text_win.get_width() // 2, win_height // 2))
            finish = True
        elif lost >= 3:
            text_lost = font0.render('u lost', 1, (255,255,255))
            window.blit(text_lost, (win_width // 2 - text_lost.get_width() // 2, win_height // 2))
            finish = True

        display.update()

    clock.tick(60)
