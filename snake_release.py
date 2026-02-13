import enum
import random as rnd
import sys

import pygame as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox

app = QApplication([])
mw = QWidget()
mw.resize(400, 200)
mw.setWindowTitle("Выбор уровня сложности")

question = QLabel('Выберете уровень сложности')
easy_btn = QPushButton('Легкий')
hard_btn = QPushButton('Сложный')
info_btn = QPushButton('Обучение')

central_line = QVBoxLayout()
central_line1 = QHBoxLayout()

central_line.addWidget(question, alignment=Qt.AlignCenter)
central_line1.addWidget(easy_btn, alignment=Qt.AlignCenter)
central_line1.addWidget(hard_btn, alignment=Qt.AlignCenter)
central_line.addLayout(central_line1)
central_line.addWidget(info_btn, alignment=Qt.AlignCenter)

difficulty = 0


class Difficulties(enum.IntEnum):
    HARD = 2
    EASY = 1


DIFFICULTIES_TO_TPS = {
    Difficulties.HARD: 12,
    Difficulties.EASY: 9
}


def set_difficulty(difficulty_to_set):
    def inner():
        global difficulty
        difficulty = difficulty_to_set
        mw.close()
        return difficulty

    return inner


def info():
    info = QMessageBox()
    info.setText(
        'Ярко-красный квадратик -- обычное яблоко\nТёмно-красный квадратик -- гнилое яблоко (отнимает 1 очко)\nРозовый квадратик -- бомба (сразу убивает)\nСиние полоски -- стены (при столкновении умираешь)\nЗелёные квадратики -- змейка (это ты)\n"H"(английская) -- рестарт на тяжолой сложности\n"E"(английская) -- рестарт на лёгкой сложности')
    info.exec_()


hard_btn.clicked.connect(set_difficulty(2))
easy_btn.clicked.connect(set_difficulty(1))
info_btn.clicked.connect(info)

mw.setLayout(central_line)
mw.show()
app.exec()

if difficulty == 0:
    sys.exit(0)

WSIZE = (720, 480)  # размер окна

screen = pg.display.set_mode(WSIZE)  # само окно

TSIDE = 20  # размер кубика
MSIZE = WSIZE[0] // TSIDE, WSIZE[1] // TSIDE  # размер карты

start_pos = MSIZE[0] // 2, MSIZE[1] // 2  # стартовая позиция змейки
snake = [start_pos]  # змейка
alive = True  # жива ли змейка

access = 0  # переменная отвечающая за нажатие одной клавиши за один игровой цикл

direction = 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # в каком направлении змека смотрит

apple = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # яблоко с рандомными координатами в пределах экрана
apple1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
apple_nig = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # гнилое яблоко
apple_nig1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # гнилое яблоко
apple_nig2 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # гнилое яблоко
apple_nig3 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # гнилое яблоко
apple_nig4 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # гнилое яблоко

# бомбы
bomb = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
bomb1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)

# стенки
wall1 = [500, 100]
wall1_x, wall1_y = 100, 100

wall2 = [400, 400]
wall2_x, wall2_y = 200, 400

clock = pg.time.Clock()  # необходимая задержка(кадры)

pg.font.init()
font_score = pg.font.SysFont("Times New Roman", 25)  # текст для счета очков
font_gameOver = pg.font.SysFont("Times New Roman", 40)  # текст для экрана проигрыша
font_restart = pg.font.SysFont("Times New Roman", 18)  # текст для перезапуска

run = True  # переменная для игрового цикла
while run:  # игровой цикл
    tps = 9

    if difficulty == Difficulties.EASY:
        tps = DIFFICULTIES_TO_TPS.get(Difficulties.EASY)
    elif difficulty == Difficulties.HARD:
        tps = DIFFICULTIES_TO_TPS.get(Difficulties.HARD)
    else:
        difficulty = Difficulties.EASY

    clock.tick(tps)

    screen.fill('black')  # заполнение фона черным

    for event in pg.event.get():
        if event.type == pg.QUIT:  # проверка на выход из игры
            run = False
        if event.type == pg.KEYDOWN:  # проверка изменения направления змейки , direction != n для того чтобы змейка
            # не заходила сама в себя
            if alive:
                if event.key == pg.K_RIGHT and direction != 2 and access == 0:
                    direction = 0
                    access = 1
                elif event.key == pg.K_DOWN and direction != 3 and access == 0:
                    direction = 1
                    access = 1
                elif event.key == pg.K_LEFT and direction != 0 and access == 0:
                    direction = 2
                    access = 1
                elif event.key == pg.K_UP and direction != 1 and access == 0:
                    direction = 3
                    access = 1
            else:
                if event.key == pg.K_h:
                    difficulty = 2
                    alive = True
                    snake = [start_pos]
                    apple = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)

                elif event.key == pg.K_e:
                    difficulty = 1
                    alive = True
                    snake = [start_pos]
                    apple = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)

    [pg.draw.rect(screen, 'darkgreen', (x1 * TSIDE, y1 * TSIDE, TSIDE - 1, TSIDE - 1)) for x1, y1 in snake]
    [pg.draw.rect(screen, 'green', (x * TSIDE, y * TSIDE, TSIDE - 1, TSIDE - 1)) for x, y in
     snake]  # отображение змейки
    pg.draw.rect(screen, 'red', (apple[0] * TSIDE, apple[1] * TSIDE, TSIDE - 1, TSIDE - 1))  # отображение яблока
    pg.draw.rect(screen, 'pink', (bomb[0] * TSIDE, bomb[1] * TSIDE, TSIDE - 1, TSIDE - 1))


    def draw_base():
        pg.draw.rect(screen, 'brown',
                     (apple_nig[0] * TSIDE, apple_nig[1] * TSIDE, TSIDE - 1, TSIDE - 1))  # отображение гнилого яблока
        pg.draw.rect(screen, 'brown',
                     (apple_nig1[0] * TSIDE, apple_nig1[1] * TSIDE, TSIDE - 1, TSIDE - 1))  # отображение гнилого яблока
        pg.draw.rect(screen, 'brown',
                     (apple_nig2[0] * TSIDE, apple_nig2[1] * TSIDE, TSIDE - 1, TSIDE - 1))  # отображение гнилого яблока


    if difficulty == Difficulties.EASY:
        pg.draw.rect(screen, 'red', (apple1[0] * TSIDE, apple1[1] * TSIDE, TSIDE - 1, TSIDE - 1))
        draw_base()

        pg.draw.rect(screen, 'blue', (wall1_x, wall1_y, wall1[0], TSIDE))
    elif difficulty == Difficulties.HARD:
        pg.draw.rect(screen, 'pink', (bomb1[0] * TSIDE, bomb1[1] * TSIDE, TSIDE - 1, TSIDE - 1))
        draw_base()

        # рисуем станы
        pg.draw.rect(screen, 'blue', (wall1_x, wall1_y, wall1[0], TSIDE))
        pg.draw.rect(screen, 'blue', (wall2_x, wall2_y, wall2[0], TSIDE))

    if alive:
        new_pos = snake[0][0] + directions[direction][0], snake[0][1] + directions[direction][
            1]  # направление и текущая позиция
        if not (0 <= new_pos[0] < MSIZE[0] and 0 <= new_pos[1] < MSIZE[
            1]) or new_pos in snake:  # проверка не вышла ли змейка за пределы экрана
            alive = False
        else:
            snake.insert(0, new_pos)  # передача змейке в голову новой позиции
            if new_pos == apple:
                apple = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)  # респавн яблока
            elif new_pos == apple1:
                apple1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            elif new_pos == bomb:
                alive = False
            elif new_pos == bomb1 and difficulty == 2:
                alive = False
            elif new_pos == apple_nig:
                apple_nig = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[
                    1] - 1)  # респавн гнилого яблоками отнимание размера у змейки
                snake.pop(-1)
                snake.pop(-1)
            elif new_pos == apple_nig1:
                apple_nig1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[
                    1] - 1)  # респавн гнилого яблоками отнимание размера у змейки
                snake.pop(-1)
                snake.pop(-1)
            elif new_pos == apple_nig2:
                apple_nig2 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[
                    1] - 1)  # респавн гнилого яблоками отнимание размера у змейки
                snake.pop(-1)
                snake.pop(-1)
            elif new_pos == apple_nig3 and difficulty == 2:
                apple_nig3 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[
                    1] - 1)  # респавн гнилого яблоками отнимание размера у змейки
                snake.pop(-1)
                snake.pop(-1)
            elif new_pos == apple_nig4 and difficulty == 2:
                apple_nig4 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[
                    1] - 1)  # респавн гнилого яблоками отнимание размера у змейки
                snake.pop(-1)
                snake.pop(-1)
            else:
                snake.pop(-1)

                # Проверка стен на столкновения с игроком, яблоком и гнилым яблоком

            if not (wall1_x // TSIDE) - 1 >= new_pos[0] and new_pos[0] <= (
                    wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= new_pos[1] <= wall1[1] // TSIDE:
                alive = False
                apple = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall1_x // TSIDE) - 1 >= apple1[0] and apple1[0] <= (wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= \
                    apple1[1] <= wall1[1] // TSIDE:
                apple1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall1_x // TSIDE) - 1 >= apple_nig[0] and apple_nig[0] <= (
                    wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= apple_nig[1] <= wall1[1] // TSIDE:
                apple_nig = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall1_x // TSIDE) - 1 >= apple_nig1[0] and apple_nig1[0] <= (
                    wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= apple_nig1[1] <= wall1[1] // TSIDE:
                apple_nig1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall1_x // TSIDE) - 1 >= apple_nig2[0] and apple_nig2[0] <= (
                    wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= apple_nig2[1] <= wall1[1] // TSIDE:
                apple_nig2 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall1_x // TSIDE) - 1 >= apple_nig3[0] and apple_nig3[0] <= (
                    wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= apple_nig3[1] <= wall1[1] // TSIDE:
                apple_nig3 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall1_x // TSIDE) - 1 >= apple_nig4[0] and apple_nig4[0] <= (
                    wall1[0] // TSIDE) + 4 and wall1_y // TSIDE <= apple_nig4[1] <= wall1[1] // TSIDE:
                apple_nig4 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)

            # вторая стена(только на втором уровне сложности)

            if not (wall2_x // TSIDE) - 1 >= new_pos[0] and new_pos[0] <= (
                    wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= new_pos[1] <= wall2[
                1] // TSIDE and difficulty == 2:
                alive = False
            if not (wall2_x // TSIDE) - 1 >= apple[0] and apple[0] <= (wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= \
                    apple[1] <= wall2[1] // TSIDE and difficulty == 2:
                apple = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall2_x // TSIDE) - 1 >= apple_nig[0] and apple_nig[0] <= (
                    wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= apple_nig[1] <= wall2[
                1] // TSIDE and difficulty == 2:
                apple_nig = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall2_x // TSIDE) - 1 >= apple_nig1[0] and apple_nig1[0] <= (
                    wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= apple_nig1[1] <= wall2[
                1] // TSIDE and difficulty == 2:
                apple_nig1 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall2_x // TSIDE) - 1 >= apple_nig2[0] and apple_nig2[0] <= (
                    wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= apple_nig2[1] <= wall2[
                1] // TSIDE and difficulty == 2:
                apple_nig2 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall2_x // TSIDE) - 1 >= apple_nig3[0] and apple_nig3[0] <= (
                    wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= apple_nig3[1] <= wall2[
                1] // TSIDE and difficulty == 2:
                apple_nig3 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)
            if not (wall2_x // TSIDE) - 1 >= apple_nig4[0] and apple_nig4[0] <= (
                    wall2[0] // TSIDE) + 9 and wall2_y // TSIDE <= apple_nig4[1] <= wall2[1] // TSIDE:
                apple_nig4 = rnd.randint(0, MSIZE[0] - 1), rnd.randint(0, MSIZE[1] - 1)

            if len(snake) == 0:  # проверка длины змейки
                alive = False
    else:

        text = font_gameOver.render(f'GAMEOVER', True, 'white')  # отрисовка текста проигрыша
        screen.blit(text, (WSIZE[0] // 2 - text.get_width() // 2, WSIZE[1] // 2 - 50))
        text = font_gameOver.render(f'Press H for restart in hard level', True, 'white')  # отрисовка текста проигрыша
        screen.blit(text, (WSIZE[0] // 2 - text.get_width() // 2, WSIZE[1] // 2 + 50))
        text = font_gameOver.render(f'Press E for restart in easy level', True, 'white')  # отрисовка текста проигрыша
        screen.blit(text, (WSIZE[0] // 2 - text.get_width() // 2, WSIZE[1] // 2 + 125))

    access = 0
    screen.blit(font_score.render(f'score: {len(snake)}', True, 'yellow'), (5, 5))  # отрисовка текста счетчика очков
    pg.display.flip()
