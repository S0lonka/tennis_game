from pygame import *
import sys


#размеры коллизии спрайта и картинки(сделано для удобства в ограничении краёв игрового поля)
picture_height = 40
picture_width  = 40


class GameSprite():
    def __init__(self, speed, width, height, p_x, p_y, color = (255,255,255)):
        self.speed = speed
        self.width = width
        self.height = height
        self.rect = Rect(p_x, p_y, width, height)
        self.rect.x = p_x
        self.rect.y = p_y
        self.color = color



    def reset(self):
        draw.rect(window, self.color, self.rect)

class Player(GameSprite):
    def update_player1(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 3:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < window_y - self.height:
            self.rect.y += self.speed

    def update_player2(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 3:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < window_y - self.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, x, y, radius):
        self.radius = radius  # Радиус круг

        #radius * 2, создаёт квадратный спрайт для круга
        #x - radius, для того чтобы центр круга совпадал с заданными координатами
        super().__init__(0, radius * 2, radius * 2, x - radius, y - radius, color=(255, 255, 255))

        self.dx = 5  # Скорость по оси x
        self.dy = 5  # Скорость по оси y

    def update_ball(self):
        #Движение мяча
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Проверка столкновения с ракетками
        self.check_collision(sprite_p1)
        self.check_collision(sprite_p2)

        # Проверка столкновения с краями экрана
        if self.rect.left < 0 or self.rect.right > window_x:
            #Поменять направление угла мяча
            self.dx *= -1

            #Мяч коснулся ЛЕВОЙ стены? (ЛЕВАЯ коллизия мяча МЕНЬШЕ 0?)
            if self.rect.left < 0:
                #Вывести надпись победил 2 игрок(справа)
                self.game_over("Player 2 wins!")

            #Мяч коснулся ПРАВОЙ стены? (ПРАВАЯ коллизия мяча БОЛЬШЕ размера окна по X?)
            elif self.rect.right > window_x:
                #Вывести надпись победил 1 игрок(слева)
                self.game_over("Player 1 wins!")
        #ВЕРХНИИ координаты мяча МЕНЬШЕ 0? или \
        # НИЖНИИ координаты мяча БОЛЬШЕ размера окна по Y
        if self.rect.top < 0 or self.rect.bottom > window_y:
            self.dy *= -1


                    #paddle = ракетка
    def check_collision(self, paddle):
        #Проверка столкновений со всеми сторонами ракетки
        if self.rect.colliderect(paddle.rect):
            # Проверка столкновения с левой стороной ракетки
            '''координата правой стороны мяча > координата левой стороны ракетки И
               координата левой стороны мяча < координата левой стороны ракетки'''
            if self.rect.right > paddle.rect.left and self.rect.left < paddle.rect.left:
                self.dx *= -1
                self.rect.right = paddle.rect.left -1  # Сдвиг мяча, чтобы не застревал

            # Проверка столкновения с правой стороной ракетки
            '''ЛЕВО мяча < ПРАВО ракетки И ПРАВО мяча > ПРАВА ракетки'''
            if self.rect.left < paddle.rect.right and self.rect.right > paddle.rect.right:
                self.dx *= -1
                self.rect.left = paddle.rect.right + 1  # Сдвиг мяча, чтобы не застревал

            # Проверка столкновения с верхней стороной ракетки
            '''НИЗ мяча > ВЕРХ ракетки И ВЕРХ мяча < ВЕРХА ракетки'''
            if self.rect.bottom > paddle.rect.top and self.rect.top < paddle.rect.top:
                self.dy *= -1
                self.rect.bottom = paddle.rect.top - 1  # Сдвиг мяча, чтобы не застревал

            # Проверка столкновения с нижней стороной ракетки
            '''ВЕРХ мяча < НИЗ ракетки И НИЗ мяча > НИЗА ракетки'''
            if self.rect.top < paddle.rect.bottom and self.rect.bottom > paddle.rect.bottom:
                self.dy *= -1
                self.rect.top = paddle.rect.bottom + 1  # Сдвиг мяча, чтобы не застревал


    #Функция вывода текста победителя и ПРОИГРЫШ
    def game_over(self, message):
        font.init()
        f1 = font.Font(None, 74)
        text = f1.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(window_x // 2, window_y // 2))
        window.blit(text, text_rect)
        display.update()
        time.wait(3000)  # Пауза на 3 секунды
        quit()
        # self.reset_game()

    def reset_game(self):
        self.rect.x = window_x / 2 - self.radius
        self.rect.y = window_y / 2 - self.radius
        self.dx = 5
        self.dy = 5
    def reset(self):
        draw.circle(window, self.color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)



#цвета
black = (0, 0, 0)
white = (255, 255, 255)

#размеры окна
window_x = 900
window_y = 640

#создай окно игры
window = display.set_mode((window_x, window_y))
display.set_caption('tennis')

#создание игрового флага
game = True
clock = time.Clock()
fps = 60

#(скорость, ширина, высота, x, y)
sprite_p1 = Player(5, 20, 70, 50, window_y / 2,)
sprite_p2 = Player(5, 20, 70, 835, window_y / 2,)

ball = Ball( window_x/2, window_y/2, 25)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    #чтобы не оставался след спрайта, заливка фона должна \
    # быть в цикле и до sprite_player.update()!
    window.fill(black)

    #Функции движения спрайтов
    sprite_p1.update_player1()
    sprite_p2.update_player2()
    #шар движение
    ball.update_ball()

    #обновление спрайтов
    sprite_p1.reset()
    sprite_p2.reset()
    #шар обновление
    ball.reset()

    #обновление экрана
    display.update()
    clock.tick(fps)

