#Подключаем модули
from random import randint
from pygame import *




#Создаем окно
win_width = 700
win_height = 500
display.set_caption("Shooter") #название
window = display.set_mode((win_width, win_height))#создаем окно
img_back = "galaxy.jpg" #фоновая картинка
background = transform.scale(image.load(img_back), (win_width, win_height)) #картинку формируем под размер окна




lost = 0 #пропущено врагов
score = 0 #набранные очки
max_lost = 3 #проиграли, если пропустили столько
goal = 10 #столько кораблей нужно сбить для победы




mixer.init()
mixer.music.load("space.ogg") #фоновая музыка
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg") #звук взрыва




#главный класс
class GameSprite(sprite.Sprite):
   #конструктор класса
    #def __init__(self, player_image, player_x, player_y, player_speed):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        #self.image = transform.scale(image.load(player_image), (55, 55))
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))








#класс-наследник для спрайта-игрока (управляется стрелками влево и вправо)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        #bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, -10)
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)




        bullets.add(bullet)








#класс для врага
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost #глобальная переменная
        #если доходит до края, то исчезает и появляется сверху
        if self.rect.y > win_height:
            self.rect.x = randint(80, 600)
            self.rect.y = 0
            lost = lost + 1 # +1 пропущенное




#класс спрайта-пули  
class Bullet(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()








img_enemy= "ufo.png" #картинка для врага
monsters = sprite.Group() #создание группы монстров
for i in range(5):
    #monster = Enemy(img_enemy, randint(80, 600), 0, randint(1,2)) #экземпляр монстра
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster) #добавление в группу




img_bullet = "bullet.png" #картинка пули
bullets = sprite.Group()








#подключение шрифтов
font.init()
font1 = font.SysFont('Arial', 80)  
font2 = font.SysFont('Arial', 36)
#надписи проигрыша и выгрыша
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))








#ship = Player("rocket.png", 350, 400, 10) #спрайт корабль
ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)




finish = False #переменная, отвечающая за окончание игры после наступления финиша и проигрыша
run = True #переменная, отвечающая за отрытие окна (оно открыто пока не нажат крестик)




#игровой цикл
while run:
    for e in event.get():
        if e.type == QUIT: #событие выхода из окна
            run = False
            #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()




    if finish != True:
        window.blit(background,(0,0))
        #текст
        text = font2.render("Счёт: " + str(score) ,1, (255,255,255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))




        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
       
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)




        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            #monster = Enemy(img_enemy, randint(80, 600), 0, randint(1,2))
            monsters.add(monster)








        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))








        #проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))




        display.update()#обновление окна




    #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()








        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            #monster = Enemy(img_enemy, randint(80, 600), 0, randint(1,2))
            monsters.add(monster)




    time.delay(10)#цикл срабатывает каждую 0.05 секунд

