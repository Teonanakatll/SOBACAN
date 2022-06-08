from tkinter import *
from time import sleep
from winsound import Beep
# ============================ КАРТА И ГРАФИКА =================================
# Сброс и пересоздание уровня
def reset():
    global moving, second, timeRun
    print("Метод reset()")
    moving = False
    second = -1
    stopTimer()
    getLevel(level)
    clear_setGrass()
    createLevel()
    updateText()

# Возвращаем строку в виде ММ:СС
def getMinSec(s):
    intMin = s // 60
    intSec = s % 60
    textSecond = str(intSec)
    if (intMin > 59):
        intMin %= 60
    if (intSec < 10):
        textSecond = "0" + textSecond
    if (intMin == 0):
        return f"{textSecond} сек."
    else:
        textMin = str(intMin)
        if (intMin < 10):
            textMin = "0" + textMin
        return f"{textMin} мин. {textSecond} сек."

# Обновляем полоску с текстом
def updateText():
    global textTime, second, timeRun
    second += 1
    cnv.delete(textTime)
    txt = f"Уровень: {level}   Прошло времени: {getMinSec(second)}"
    textTime = cnv.create_text(10, 10, fill="#FFCAAB", anchor="nw",
                               text=txt, font="Verdana, 15")
    timeRun = root.after(1000, updateText)

# Останавливаем таймер
def stopTimer():
    global timeRun
    if (timeRun != None):
        root.after_cancel(timeRun)
        timeRun = None

# Загрузка данных уровня
def getLevel(lvl):
    global dataLevel
    print("Метод getLevel()")
    dataLevel = []
    tmp = []

    idx = str(lvl)
    if (lvl < 10):
        idx = f"0{lvl}"
    try:
        f = open(f"levels/level{idx}.dat", "r", encoding="utf-8")
        for i in f.readlines():
            tmp.append(i.replace("\n", ""))
            f.close()
        for i in range(len(tmp)):
            dataLevel.append([])
            for j in tmp[i]:
                dataLevel[i].append(int(j))
    except:
        print("Не найден файл с данными.")
        quit(0)

# Замостить изображением grass.png всю область окна
def clear_setGrass():
    print("Метод clear_setGrass()")
    cnv.delete(ALL)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            cnv.create_image(SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                             SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                             image=backGround)

# Создание обьектов в Canvas
def createLevel():
    print("Метод createLevel()")
    global player, boxes, finish
    player = []
    boxes = []
    finish = []

    for i in range(len(dataLevel)):
        for j in range(len(dataLevel[i])):
            if (dataLevel[i][j] == 1):
                cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                 SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                 image=img[0])
            elif (dataLevel[i][j] == 3):
                dataLevel[i][j] = 0
                finish.append([i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                                      SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                                      image=img[2]), False])


    for i in range(len(dataLevel)):
        for j in range(len(dataLevel[i])):
            if (dataLevel[i][j] == 2):
                dataLevel[i][j] = 0
                boxes.append([i, j,
                              cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                               SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                               image=img[1])])
            elif (dataLevel[i][j] == 4):
                dataLevel[i][j] = 0
                player = [i, j, cnv.create_image(SQUARE_SIZE // 2 + j * SQUARE_SIZE,
                                                 SQUARE_SIZE // 2 + i * SQUARE_SIZE,
                                                 image=img[3][1])]

    for i in range(len(finish)):
        print(finish[i])
                                               
# =========================== УПРАВЛЕНИЕ И ДВИЖЕНИЕ ===========================

# Обработка нажатий клавиш
def move(v):
    print("Метод move()")

    if (moving):
        return 0
    cnv.delete(player[2])
    player[2] = cnv.create_image(SQUARE_SIZE // 2 + player[1] * SQUARE_SIZE,
                                 SQUARE_SIZE // 2 + player[0] * SQUARE_SIZE,
                                 image=img[3][v])

    x = player[0]
    y = player[1]
    Beep(625, 10)

    if (v == UPKEY):
        check = getNumber(x - 1, y)
        if (check == 0):
            movePlayerTo(0, -8, 8)
            player[0] -= 1
        elif (check == 2):
            nextCheck = getNumber(x - 2, y)
            if (nextCheck == 0):
                numberBox = getBox(x - 1, y)
                movePlayerBoxTo(0, -8, 8, numberBox)
                player[0] -= 1
                boxes[numberBox][0] -= 1
    elif (v == DOWNKEY):
        check = getNumber(x + 1, y)
        if (check == 0):
            movePlayerTo(0, 8, 8)
            player[0] += 1
        elif (check == 2):
            nextCheck = getNumber(x + 2, y)
            if (nextCheck == 0):
                numberBox = getBox(x + 1, y)
                movePlayerBoxTo(0, 8, 8, numberBox)
                player[0] += 1
                boxes[numberBox][0] += 1
    elif (v == LEFTKEY):
        check = getNumber(x, y - 1)
        if (check == 0):
            movePlayerTo(-8, 0, 8)
            player[1] -= 1
        elif (check == 2):
            nextCheck = getNumber(x, y - 2)
            if (nextCheck == 0):
                numberBox = getBox(x, y - 1)
                movePlayerBoxTo(-8, 0, 8, numberBox)
                player[1] -= 1
                boxes[numberBox][1] -= 1
    elif (v == RIGHTKEY):
        check = getNumber(x, y + 1)
        if (check == 0):
            movePlayerTo(8, 0, 8)
            player[1] += 1
        elif (check == 2):
            nextCheck = getNumber(x, y + 2)
            if (nextCheck == 0):
                numberBox = getBox(x, y + 1)
                movePlayerBoxTo(8, 0, 8, numberBox)
                player[1] += 1
                boxes[numberBox][1] += 1

# Проверка клетки
def getNumber(x, y):
    print("Функция getNumber()")
    for box in boxes:
        if (box[0] == x and box[1] == y):
            return 2
    if (dataLevel[x][y] <= 1):
        return dataLevel[x][y]

# Функция возвращающая номер яшика
def getBox(x, y):
    print("Функция getBox()")
    for i in range(len(boxes)):
        if (boxes[i][0] == x and boxes[i][1] == y):
            return i
    return None

# Перемещение погрузчика
def movePlayerTo(x, y, count):
    global moving
    count -= 1
    cnv.move(player[2], x, y)

    if (count > 0):
        moving = True
        root.after(20, lambda x=x, y=y, c=count: movePlayerTo(x, y, c))
    else:
        print("Метод movePlayerTo() выполнился")
        moving = False

# Перемещение погрузчика с ящиком
def movePlayerBoxTo(x, y, count, numberBox):
    global moving
    count -= 1
    cnv.move(player[2], x, y)
    cnv.move(boxes[numberBox][2], x, y)

    if (count > 0):
        moving = True
        root.after(20, lambda x=x, y=y, c=count,
                   n=numberBox: movePlayerBoxTo(x, y, c, n))
    else:
        print("Метод movePlayerBoxTo() выполнен")
        moving = False
        checkBoxInFinish()

# Проверка выигрыша
def checkBoxInFinish():
    global finish, win
    print("Метод checkBoxInFinish()")

    for fin in finish:
        fin[3] = False

    win = True
    fin = 0
    while (fin < len(finish) and win):
        box = 0
        while (box < len(boxes)):
            if (finish[fin][0:2] == boxes[box][0:2]):
                finish[fin][3] = True
                box = len(boxes)
            box += 1
        win = win and finish[fin][3]
        fin += 1

    if (win):
        Beep(750, 10)
        Beep(1750, 10)
        nextLevel()

# Новый уровень
def nextLevel():
    print("Метод nextLevel()")
    cnv.delete(ALL)
    stopTimer()

    btnCheat.place(x=-100, y=-100)
    btnReset.place(x=-100, y=-100)
    btnNext = Button(text="Продолжить", font="Verdana, 19", width=45)
    btnNext.place(x=300, y=550)
    btnNext.focus_set()
    btnNext["command"] = lambda b=btnNext: nextLevelSet(b)

    cnv.create_text(WIDTH * SQUARE_SIZE // 2, 200, fill="#AAFFCC",
                    text=f"Победа! Вы собрали головоломку за {getMinSec(second)}! Поздравляем!",
                    font="Verdana, 25")

# Переключение уровня
def nextLevelSet(btnNext: Button):
    global level
    level += 1
    cnv.focus_set()
    btnNext.destroy()
    btnCheat.place(x=10, y = 590)
    btnReset.place(x=10, y = 550)
    cnv.delete(ALL)
    reset()

# Чит кнопка
def goCheat():
    global moving
    print("Метод go Cheat()")
    moving = True
    for i in range(len(boxes)):
        boxes[i][0] = finish[i][0]
        boxes[i][1] = finish[i][1]
        cnv.coords(boxes[i][2],
                   SQUARE_SIZE // 2 + boxes[i][1] * SQUARE_SIZE,
                   SQUARE_SIZE // 2 + boxes[i][0] * SQUARE_SIZE)
        cnv.update()
        sleep(2)
        checkBoxInFinish()


# =============================================================================
root = Tk()
root.resizable(False, False)
root.title("Кособан v. 3.3672 alpha beta super")
root.iconbitmap("icon/icon.ico")

WIDTH = 20
HEIGHT = 10
SQUARE_SIZE = 64

POS_X = root.winfo_screenwidth() // 2 - (WIDTH * SQUARE_SIZE) // 2
POS_Y = root.winfo_screenheight() // 2 - (HEIGHT * SQUARE_SIZE) // 2
root.geometry(f"{WIDTH * SQUARE_SIZE + 0}x{HEIGHT * SQUARE_SIZE + 0}+{POS_X}+{POS_Y}")

# Коды нажатых клавиш
UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

# Канвас
cnv = Canvas(root, width=WIDTH * SQUARE_SIZE, height=HEIGHT * SQUARE_SIZE, bg="#373737")
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

# Клавиши управления
cnv.bind("<Up>", lambda e, x=UPKEY: move(x))
cnv.bind("<Down>", lambda e, x=DOWNKEY: move(x))
cnv.bind("<Left>", lambda e, x=LEFTKEY: move(x))
cnv.bind("<Right>", lambda e, x=RIGHTKEY: move(x))

# Анимация погрузчика работает?
moving = True

# Список с изображениями
img = []
img.append(PhotoImage(file="image/wall.png"))
img.append(PhotoImage(file="image/box.png"))
img.append(PhotoImage(file="image/finish.png"))
img.append([])
img[3].append(PhotoImage(file="image/kosoban_up.png"))
img[3].append(PhotoImage(file="image/kosoban_down.png"))
img[3].append(PhotoImage(file="image/kosoban_left.png"))
img[3].append(PhotoImage(file="image/kosoban_right.png"))

# Переменные обьектов
player = None
boxes = None
finish = None

# Переменные времени
textTime = None
second = None

# Обьект для хранения вызова с помощью .after()
timeRun = None

# Уровень и математическая модель уровня
level = 5
dataLevel = []

# Текстура травы
backGround = PhotoImage(file="image/grass.png")

# Победа?
win = False

# Кнопки управления
btnReset = Button(text="Сбросить поле".upper(),
                  font="Consolas 15", width=20)
btnReset.place(x=10, y=550)
btnReset["command"] = reset

btnCheat = Button(text="Установить ящики".upper(),
                  font="Consolas 15", width=20)
btnCheat.place(x=10, y=590)
btnCheat["command"] = goCheat

reset()
root.mainloop()
