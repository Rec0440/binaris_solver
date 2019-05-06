''' містить функції перевірки матриці'''
def need_filling(m):
    ''' Чи потрібно ще заповнювати матрицю - повертає True/False '''
    flag = False
    for x in m:
        if '*' in x:
            flag = True
            break
    return flag

def everything_ok(m, msize, max_digit):
    ''' чи порушуються правила гри - повертає True/False '''
    rule = True          # rule of game
    for x in m:                  # перевіряємо чи не забагато 0/1 в рядочку
        k0 = x.count('0')             # .count - стандартний метод стрічкового типу даних
        k1 = x.count('1')
        if k0 > max_digit or k1 > max_digit:
            rule = False
            return rule # вихід, якщо є порушення правила
    for x in range(msize):       # в колонці
        col = [row[x] for row in m]
        k0 = col.count('0')
        k1 = col.count('1')
        if k0 > max_digit or k1 > max_digit:
            rule = False
            return rule
    for x in m:          # перевіряємо чи є три цифри підряд в рядочку
        if '000' in x:
            rule = False
            return rule
        if '111' in x:
            rule = False
            return rule
    for x in range(msize):      # в колонці
        col = [row[x] for row in m]
        col = ''.join(col)
        if '000' in col:
            rule = False
            return rule
        if '111' in col:
            rule = False
            return rule
    # чи не має однакових рядочків, схема порівняння - 0 ws 1-5, 1 ws 2-5, 2 ws 3-5, 3 ws 4-5, 4 ws 5
    for y in range(msize-1):
        if '*' in m[y]: # НЕ звіряти взагалі всі рядки з *
            continue
        for x in range(y+1, msize):
            if m[y] == m[x]:
                rule = False
                return rule
    for y in range(msize-1):     # колонок
        col_y = [row[y] for row in m]    # Получить элементы row[y] из каждой строки матрицы m и создать из них новый список
        if '*' in col_y:
            continue
        for x in range(y+1, msize):
            col_x = [row[x] for row in m]
            if col_y == col_x:
                rule = False
                return rule
    return rule

def check_task(m):
    ''' Перевірити розмір рядочків, чи однакової довжини,
    чи введені допустимі символи 0, 1, * '''
    stat = True
    size = len(m)
    for x in range(size):
        if len(m[x]) != size:
            stat = False
        for y in range(size):
            if not(m[x][y] in ('*', '1', '0')):
                stat = False
    return stat