'''Вирішувач головоломки binaris 1001 (PlayMarket)
   правила гри:              в колонці або в рядочку однакова кількість 0 і 1
                             поряд може бути не більше двох однакових символів
                             не має однакових колонок чи рядочків
   завдання подати у файлі task.txt'''

import time
import data.check
import data.rules

print()
# ініціалізація змінних
file_g = 'task.txt'              # назва файлу
М = []                           # оригінал матриці з початковим завданням
msize = 0                        # розмір поля, він же розмір рядочка/колонки
max_digit = 0                    # Макисмальна кількість нулів/одиниць у рядочку/колонці
matrix_stack = []                # стек матриць
move = []                        # випадковий хід - номер ряждочка [0], позиція в рядочку [1], значення 0/1 [2]
rules_ok = None                  # чи відповідає матриця правилам
need_fill_M = None               # чи потрібно ще щаповнювати матрицю
cicle = None                     # чи ми зациклились
end = None                       # змінна головного циклу


def generate_new_game(f):
    '''Старт гри,
    зчитування завдання, створення робочої матриці'''
    game_matrix = []
    task_file = open(f, 'r')
    line = task_file.readline()
    line = line.rstrip()
    size = len(line)
    count = int(size // 2)
    while line != '':
        game_matrix.append(line)
        line = task_file.readline()
        line = line.rstrip()
    task_file.close()
    return game_matrix, size, count

def print_matrix(m):
    '''друк матриці'''
    for x in m:
        print('   ', x)
    print()
    
def check_status(m0, m1, msize, max_digit):
    ''' повертає значення основних індикаторів роботи програми'''
    rules_ok = data.check.everything_ok(m1, msize, max_digit)         # чи матриця відповідає правилам?
    need_fill_M = data.check.need_filling(m1)                         # чи потрібно заповнити матрицю?
    cicle = True if m0 == m1 else False                               # перевірка на зациклюваність
    return rules_ok, need_fill_M, cicle

def random_move(m):
    '''вибрає випадковий хід,
    допрацювати логіку!!!!'''
    index = -1
    x = -1
    a = m[:]
    s = len(m)
    while index <= -1 or x == s:
        x += 1
        index = m[x].find('*')
    a[x] = m[x][:index] + '0' + m[x][index+1:]
    if data.check.everything_ok(a, msize, max_digit):
        move = [x, index, '0']
    else:
        move = [x, index, '1']
    return move

def opos_move(move):
    ''' повертає протилежний хід'''
    opmove = move[:]
    opmove[2] = '1' if opmove[2] == '0' else '0'
    return opmove

def whmove(end, m):
    '''блок прийняття рішення
    як діяти, коли немає очевидних ходів'''
    item = None
    if rules_ok:  # правила заповнення матриці Ok
        if need_fill_M:  # матриця НЕзаповнена
            if not (cicle):  # ми не зациклились і продовжуємо шукати розв'язок
                return end, m
            else:  # ми ЗАЦИКЛИЛИСЬ. спробуємо хід навмання
                move = random_move(m)  # обираємо випадковий хід - move = (x, y, digit)
                item = m[:]
                item[move[0]] = m[move[0]][:move[1]] + opos_move(move)[2] + m[move[0]][move[1]+1:]
                matrix_stack.append(item)
                m[move[0]] = m[move[0]][:move[1]] + move[2] + m[move[0]][move[1]+1:]
                return end, m
        else:  # матриця ЗАПОВНЕНА, ми знайшли розвязок
            print('\nWe find solution!\n')
            end = True
            return end, m
    else:  # правила заповнення НЕДОТРИМАНІ
        if len(matrix_stack) == 0:
            print('We have no move. General ERROR, need debuging!')  # ПОМИЛКА!!!
            end = True
            return end, m
        else:  # якщо були ходи навмання
            m = matrix_stack.pop()     # забрати зі стеку останню правильну матрицю    
    return end, m



M, msize, max_digit = generate_new_game(file_g)     # стартова процедура
status = data.check.check_task(M)                   # Перевіряємо правильність подачі завдання
end = False if status == True else True             # змінна головного циклу
print('The task was:')
print_matrix(M)
t1 = time.time()                                    # засікаємо час початку роботи алгоритму

while not(end):
    m0 = M[:]                                             # Зберігаємо робочу матрицю до обробки
    M = data.rules.through_the_rules(M, msize, max_digit) # пропускаємо матрицю через всі відомі правила розвязку 1 раз
    m1 = M[:]                                             # Зберігаємо робочу матрицю після обробки
    rules_ok, need_fill_M, cicle = check_status(m0, m1, msize, max_digit) # перевіряємо індикатори роботи програми
    end, M = whmove(end, M)# блок прийняття рішення

t2 = time.time()                    # фіксуємо час закінчення роботи
print_matrix(M)                     # друкуємо результат
print('Done ws {0:.4f}c'.format(t2-t1))