class BoardException (Exception):  # исключения
    pass
class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы стреляете мимо доски!!! Улучшите свою точность!'
class BoardUsedException(BoardException):
    def __str__(self):
        return ('Два раза в цель снаряд не падает! Давайте новую точку!!!')
class BoardWrongShipException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f'Dot({self.x},{self.y})'

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow #Расположение носа
        self.l = l #Длина коробля
        self.o = o #вертикаль или горизонталь
        self.lives = l #кол-во жизней

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):# цикл по длине корабля
            cur_x = self.bow.x# координата у корабля
            cur_y = self.bow.y# координата х корабля
            if self.o == 0: #если по горизонтали
                cur_x += i
            elif self.o == 1:# если по вертикали
                cur_y += i
            ship_dots.append(Dot(cur_x,cur_y))
            return ship_dots #точки корабля

    def shooten(self,shot):
        return shot in self.dots

class Board:
    def __init__(self,hid = False, size = 6):
        self.hid = hid #отображение (или нет) корабля
        self.size = size # размер поля

        self.count = 0

        self.field = [['0'] * size for _ in range(size)] # заполнение поля нулями

        self.ships = [] #клетки на которых корабли
        self.busy = [] #клетки на которые заняты либо выстрелом, либо кораблем

    def __str__(self): # заполнение поля нумерацией
        res = ''
        res +='  | 1 | 2 | 3 | 4 | 5 | 6 | '
        for i, row in enumerate(self.field):
            res +=f'\n{i+1} | ' + ' | '.join(row) + ' | '
        if self.hid:
            res = res.replace(" ■ ", " O ")
        return res

    def out(self,d):  # Проверка выхода за границы поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self,ship, verb = False):
        near = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)]  # точки которые нельзя занимать другими кораблями, возле другого корабля
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ships(self,ship):  # ставим корабль на доску
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
            self.ships.append(ship)
            self.contour(ship)
    def shot(self,d): # производим выстрел
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Вы потопили корабль! Поздравляю!')
                    return False
                else:
                    print('Вы попали по кораблю! Осталось чуть-чуть и он будет потоплен!!!')
                    return True
        print('Вы промахнулись! Цельтесь лучше!')
        self.field[d.x][d.y] = '.'
        return False
    def begin(self):
        self.busy = []








