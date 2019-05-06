''' містить правила заповнення матриці в рядочках '''
def fill_in_row_by_1or0(m, msize, max_digit, x_int):
    ''' Заповнення всіх вільних місць в рядочку одиницями або нулями '''
    if m[x_int].count('0') == max_digit:                         # якщо '0'ки в рядочку вже всі стоять
        for y in range(msize):                                   # то заповнити всі вільні мвсця .1.
            if m[x_int][y] == '*':
                m[x_int] = m[x_int][:y] + '1' + m[x_int][y+1:]   # якщо 1й або 3й доданки не існують, то доданок поретворюється у ''
    if m[x_int].count('1') == max_digit:                         # якщо '1'ки в рядочку вже всі стоять
        for y in range(msize):                                   # # то заповнити всі вільні місця '0'ми
            if m[x_int][y] == '*':
                m[x_int] = m[x_int][:y] + '0' + m[x_int][y+1:]
    return m

def fill_in_row_by_010or101(m, x_int):
    ''' Заповнює одиницею/нулем  проміжок 0*0/1*1 в рядочку '''
    digit = '1*1'                                                 # шукаємо комбінацію 1*1 і вставляємо 0
    index = m[x_int].find(digit)
    while index >= 0:
        m[x_int] = m[x_int][:index+1] + '0' + m[x_int][index+2:]      # якщо 1й або 3й доданки не існують, то доданок поретворюється у ''
        index = m[x_int].find(digit, index+2)                         # спроба знайти наступне співпадіння
    digit = '0*0'                                                 # шукаємо комбінацію 0*0 і вставляємо 1
    index = m[x_int].find(digit)
    while index >= 0:
        m[x_int] = m[x_int][:index+1] + '1' + m[x_int][index+2:]
        index = m[x_int].find(digit, index+2)
    return m

def fill_in_row_by_0110or1001(m, x_int):
    ''' доповнює всі комбінації 00 та 11 на 1001 та 0110 '''
    comb = ['00*', '11*', '*00', '*11']         # список шуканих комбінацій
    tick = 0                                    # ітератор комбінацій
    pos_comb = -1                               
    while pos_comb < 0 and tick < 4: # поки не перестанемо знаходити, та не переберем всі комбінації - повторювати
        pos_comb = m[x_int].find(comb[tick])     # шукаємо комбінацію
        if pos_comb > -1:                        # якщо комбінація знайдена
            if tick in (0, 1):                        # якщо це 00* або 11*
                digit = '1' if tick == 0 else '0'         # то присвоїти відповідний символ для заповнення
                # якщо 1й або 3й доданки не існують, то доданок поретворюється у ''
                m[x_int] = m[x_int][:pos_comb+2] + digit + m[x_int][pos_comb+3:] 
                pos_comb = -1                             # спробуємо знайти ще раз
            elif tick in (2, 3):                      # якщо це *00 або *11
                digit = '1' if tick == 2 else '0'         # то присвоїти відповідний символ для заповнення
                m[x_int] = m[x_int][:pos_comb] + digit + m[x_int][pos_comb+1:]
                pos_comb = -1
        else:                                    # якщо комбінація не знайдена перейти до наступної
            tick += 1
    return m

def fill_1_in_0xxx10(m, msize, max_digit, x_int):
    ''' три підряд '1' в **1 стояти не можуть, отже там 100% є хоча б один нулик'''
    if m[x_int].count('*') > 2:      # якщо існує мінімальна можливість шуканої ситуації
        index = 0                         # позиція в стрічці пошуку комбінації
        comb = ['**1', '*1*', '1**']      # шукані комбінації
        count_poseb_0 = 0                 # кількість окремих непересічних комбінацій
        bank_index = []                   # список позицій в стрічці знайдених комбінацій
        while index < msize-2:                 # поки індекс не дійшов до кінця стрічки ...
            tick = 0
            while tick < 3:                       # поки не перебрані всі комбінації
                pos_comb = m[x_int].find(comb[tick], index)    # шукати потрібну комбінацію в стрічці
                if pos_comb > -1:                              # якщо комбінацію знайшли
                    bank_index.append(pos_comb)                         # додати її у список
                    bank_index.append(pos_comb+1)
                    bank_index.append(pos_comb+2)
                    index = pos_comb + 3
                    count_poseb_0 += 1        # фіксуємо знайдену комбінацію
                    tick = -1
                tick += 1                
            else:
                break   # якщо так і не вдалось знайти хоча б одну комбінацію - вийти з пошуку
        if bank_index == []:
            return m                     # якщо не знайдена жодна комбінація, закінчити пошук і вийти
        left_1 = max_digit - m[x_int].count('1')   # скільки залишилось поставити одиничок, чи вистарчить їх на знайдені комбінації?
        left_0 = max_digit - m[x_int].count('0')   # скільки всього залишилось поставити нулів
        if left_0 == count_poseb_0 and left_1 >= count_poseb_0 * 2:
        # якщо кількість комбінації, де 100% має стояти нулик дорівнює кількості потрібних стрічці нулів,
        # і для цього достатньо одиничок
            for y in range(msize):
                if not(y in bank_index):
                    if m[x_int][y] == '*':
                        m[x_int] = m[x_int][:y] + '1' + m[x_int][y + 1:]  # то вставити по цьому правилу
    return m

def fill_0_in_1xxx01(m, msize, max_digit, x_int):
    ''' три підряд '0' в **0 стояти не можуть, отже там 100% є хоча б одна одиниця!! '''
    if m[x_int].count('*') > 2:      # якщо існує мінімальна можливість шуканої ситуації
        index = 0                         # позиція в стрічці пошуку комбінації
        comb = ['**0', '*0*', '0**']      # шукані комбінації
        count_poseb_1 = 0                 # кількість окремих непересічних комбінацій
        bank_index = []                   # список позицій в стрічці знайдених комбінацій
        while index < msize-2:                 # поки індекс не дійшов до кінця стрічки ...
            tick = 0
            while tick < 3:                       # поки не перебрані всі комбінації
                pos_comb = m[x_int].find(comb[tick], index)    # шукати потрібну комбінацію в стрічці
                if pos_comb > -1:                              # якщо комбінацію знайшли
                    bank_index.append(pos_comb)                         # додати її у список
                    bank_index.append(pos_comb+1)
                    bank_index.append(pos_comb+2)
                    index = pos_comb + 3
                    count_poseb_1 += 1        # фіксуємо знайдену комбінацію
                    tick = -1
                tick += 1                
            else:
                break   # якщо так і не вдалось знайти хоча б одну комбінацію - вийти з пошуку
        if bank_index == []:
            return m                     # якщо не знайдена жодна комбінація, закінчити пошук і вийти
        left_0 = max_digit - m[x_int].count('0')
        left_1 = max_digit - m[x_int].count('1')
        if left_1 == count_poseb_1 and left_0 >= count_poseb_1 * 2:
        # якщо кількість комбінації, де 100% має стояти нулик дорівнює кількості потрібних стрічці нулів,
        # і для цього достатньо одиничок
            for y in range(msize):
                if not(y in bank_index):
                    if m[x_int][y] == '*':
                        m[x_int] = m[x_int][:y] + '0' + m[x_int][y + 1:]  # то вставити по цьому правилу
    return m

def coincidence_in_row(m, msize, x):
    def count_coincidence_in_row(m, msize, x, coinc_int):
        ''' Перевіряє рядочок m[x] на співпадіння з іншими рядочками '''
        cid = 0                                       # лічильник співпадінь
        for y in range(msize):                        # лічильник рядочків
            if x != y and m[y].count('*') == 0:       # Якщо рядочок порівняння не той самий і він заповнений
                for index in range(msize):            # лічильник позиції в рядочку
                    if m[x][index] == m[y][index]:    # є співпадіння?
                        cid +=1
                if cid == msize-coinc_int:            # якщо кількість співпадінь = розмір рядочка - кількість зірочок
                    return y                 # повернути результат, потрібний рядочок знайдений
                else:
                    cid = 0
        return -1                            # рядочок не знайдений
    def fill_in_coincid_row(m, x, row_coincid, coinc_int):
        if coinc_int == 2:
            ind = m[x].find('*')
            if m[row_coincid][ind] == '0':
                m[x] = m[x][:ind] + '1' + m[x][ind+1:]
            else:
                m[x] = m[x][:ind] + '0' + m[x][ind+1:]
        elif coinc_int == 3:
            ind_1 = m[x].find('*')
            ind_2 = m[x].find('*', ind_1+1)
            ind_3 = m[x].find('*', ind_2+1)
            if m[row_coincid][ind_1] == '0' and m[row_coincid][ind_2] == '0':
                m[x] = m[x][:ind_3] + '0' + m[x][ind_3 + 1:]
            elif m[row_coincid][ind_1] == '0' and m[row_coincid][ind_3] == '0':
                m[x] = m[x][:ind_2] + '0' + m[x][ind_2 + 1:]
            elif m[row_coincid][ind_2] == '0' and m[row_coincid][ind_3] == '0':
                m[x] = m[x][:ind_1] + '0' + m[x][ind_1 + 1:]
            elif m[row_coincid][ind_1] == '1' and m[row_coincid][ind_2] == '1':
                m[x] = m[x][:ind_3] + '1' + m[x][ind_3 + 1:]
            elif m[row_coincid][ind_1] == '1' and m[row_coincid][ind_3] == '1':
                m[x] = m[x][:ind_2] + '1' + m[x][ind_2 + 1:]
            elif m[row_coincid][ind_2] == '1' and m[row_coincid][ind_3] == '1':
                m[x] = m[x][:ind_1] + '1' + m[x][ind_1 + 1:]
        return m
    # порівнюємо вже заповнені з таким самим з 2ма * - на одне з незаповнених місць дати протилежний символ
    coinc = m[x].count('*')
    if coinc in (2, 3):                                         # шукаємо в активному рядку 2 або три **
        # шукаємо рядок з відповідною кількістю співпадінь: 2 = msize-2, 3 = msize-3
        cid_row = count_coincidence_in_row(m, msize, x, coinc)
        if  cid_row != -1:                                      # якщо знайшли 
            m = fill_in_coincid_row(m, x, cid_row, coinc)        # додаємо протилежний символ, cidenc - лічильник неспівпадінь
    return m