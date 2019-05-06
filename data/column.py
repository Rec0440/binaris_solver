''' містить правила заповнення матриці в колонках'''

def fill_in_col_by_1or0(m, msize, max_digit, x_int):
    col = [row_1[x_int] for row_1 in m]
    col = ''.join(col)
    if col.count('0') == max_digit:                           # якщо всі '1' в колонці вже стоять
        for y in range(msize):            # y - це позиція в колонці знайденого елемента, а, отже, це номер рядка
            if col[y] == '*':             # x_int - це позиція в рядку  - m[y][x_int] = '*'
                m[y] = m[y][:x_int] + '1' + m[y][x_int+1:]
    elif col.count('1') == max_digit:                         # якщо всі '0' в колонці вже стоять
        for y in range(msize):            # y - це позиція в колонці знайденого елемента, а, отже, це номер рядка
            if col[y] == '*':             # x_int - це позиція в рядку  - m[y][x_int] = '*'
                m[y] = m[y][:x_int] + '0' + m[y][x_int+1:]
    return m

def fill_in_col_by_010or101(m, x_int):
    ''' Заповнення нулем/одиницею знайдену комбінацію 1*1/0*0 в колонці '''
    col = [row_1[x_int] for row_1 in m]
    col = ''.join(col)    
    index = col.find('0*0')               # index+1 це рядочок, де змінити * на 1, а х_int - це позиція в рядочку
    if index > -1:
        m[index+1] = m[index + 1][:x_int] + '1' + m[index + 1][x_int + 1:]
    index = col.find('1*1')
    if index > -1:
        m[index+1] = m[index + 1][:x_int] + '0' + m[index + 1][x_int + 1:]
    return m

def fill_in_col_by_0110or1001(m, x_int):
    ''' Заповнення нулем/одиницею знайдену комбінацію *11*/*00* в колонці '''
    col = [row_1[x_int] for row_1 in m]
    col = ''.join(col)
    index = col.find('00*')               # index+1 це рядочок, де змінити * на 1, а х_int - це позиція в рядочку
    if index > -1:
        m[index+2] = m[index+2][:x_int] + '1' + m[index+2][x_int+1:]
    index = col.find('11*')
    if index > -1:
        m[index+2] = m[index+2][:x_int] + '0' + m[index+2][x_int+1:]
    index = col.find('*00')
    if index > -1:
        m[index] = m[index][:x_int] + '1' + m[index][x_int+1:]
    index = col.find('*11')
    if index > -1:
        m[index] = m[index][:x_int] + '0' + m[index][x_int+1:]
    return m

def fill_in_col_0xxx10(m, msize, max_digit, x_int):
    ''' три підряд '1' в **1 стояти не можуть, отже там 100% є хоча б один нулик'''
    col = [row_1[x_int] for row_1 in m]
    col = ''.join(col)
    # Працює погано!!!!!!!!!!!
    if col.count('*') > 2:      # якщо існує мінімальна можливість шуканої ситуації
        index = 0                         # позиція в стрічці пошуку комбінації
        comb = ['**1', '*1*', '1**']      # шукані комбінації
        count_poseb_0 = 0                 # кількість окремих непересічних комбінацій
        bank_index = []                   # список позицій в стрічці знайдених комбінацій
        while index < msize-2:                 # поки індекс не дійшов до кінця стрічки ...
            tick = 0
            while tick < 3:                       # поки не перебрані всі комбінації
                pos_comb = col.find(comb[tick], index)    # шукати потрібну комбінацію в стрічці, починаючи з позиції index
                if pos_comb > -1:                              # якщо комбінацію знайшли
                    bank_index.append(pos_comb)
                    bank_index.append(pos_comb+1)
                    bank_index.append(pos_comb+2)
                    count_poseb_0 += 1
                    index = pos_comb + 3
                    tick = -1
                tick += 1                
            else:
                break   # якщо так і не вдалось знайти хоча б одну комбінацію - вийти з пошуку
        if bank_index == []:
            return m                     # якщо не знайдена жодна комбінація, закінчити пошук і вийти
        left_1 = max_digit - col.count('1')   # скільки залишилось поставити одиничок, чи вистарчить їх на знайдені комбінації?
        left_0 = max_digit - col.count('0')   # скільки всього залишилось поставити нулів
        if left_0 == count_poseb_0 and left_1 >= count_poseb_0 * 2:
        # якщо кількість комбінації, де 100% має стояти нулик дорівнює кількості потрібних стрічці нулів,
        # і для цього достатньо одиничок
            for y in range(msize):
                if not(y in bank_index):
                    if col[y] == '*':                               # y - це позиція в колонці знайденого елемента, а, отже, це номер рядка
                        m[y] = m[y][:x_int] + '1' + m[y][x_int+1:]  # x_int - це позиція в рядку  - m[y][x_int] = '*'
    return m

def fill_in_col_1xxx01(m, msize, max_digit, x_int):
    ''' три підряд '0' в **0 стояти не можуть, отже там 100% є хоча б одна одиничка'''
    col = [row_1[x_int] for row_1 in m]
    col = ''.join(col)

    if col.count('*') > 2:      # якщо існує мінімальна можливість шуканої ситуації
        index = 0                         # позиція в стрічці пошуку комбінації
        comb = ['**0', '*0*', '0**']      # шукані комбінації
        count_poseb_1 = 0                 # кількість окремих непересічних комбінацій
        bank_index = []                   # список позицій в стрічці знайдених комбінацій
        while index < msize-2:                 # поки індекс не дійшов до кінця стрічки ...
            tick = 0
            while tick < 3:                       # поки не перебрані всі комбінації
                pos_comb = col.find(comb[tick], index)    # шукати потрібну комбінацію в стрічці, починаючи з позиції index
                if pos_comb > -1:                              # якщо комбінацію знайшли
                    bank_index.append(pos_comb)
                    bank_index.append(pos_comb+1)
                    bank_index.append(pos_comb+2)
                    count_poseb_1 += 1
                    index = pos_comb + 3
                    tick = -1
                tick += 1                
            else:
                break   # якщо так і не вдалось знайти хоча б одну комбінацію - вийти з пошуку
        if bank_index == []:
            return m                     # якщо не знайдена жодна комбінація, закінчити пошук і вийти
        left_1 = max_digit - col.count('1')   # скільки залишилось поставити одиничок, чи вистарчить їх на знайдені комбінації?
        left_0 = max_digit - col.count('0')   # скільки всього залишилось поставити нулів
        if left_1 == count_poseb_1 and left_0 >= count_poseb_1 * 2:
        # якщо кількість комбінації, де 100% має стояти нулик дорівнює кількості потрібних стрічці нулів,
        # і для цього достатньо одиничок
            for y in range(msize):
                if not(y in bank_index):
                    if col[y] == '*':                               # y - це позиція в колонці знайденого елемента, а, отже, це номер рядка
                        m[y] = m[y][:x_int] + '0' + m[y][x_int+1:]  # x_int - це позиція в рядку  - m[y][x_int] = '*'
    return m

def coincidence_in_col(m, msize, x_int):
    col = [row_1[x_int] for row_1 in m]
    col = ''.join(col)    
    def count_coincidence_in_col(m, x, coinc_int):
        ''' Перевіряє колонку col на співпадіння з іншими колонками '''
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

    def fill_in_coincid_col(m, x, row_coincid, coinc_int):
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
    
    # створюємо матрицю колонок для пошуку подібності
    m_col = []
    for y in range(msize):
        col_1 = [colum[y] for colum in m]
        col_1 = ''.join(col_1)
        m_col.append(col_1)
        
    # порівнюємо вже заповнені з таким самим з 2ма * - на одне з незаповнених місць дати протилежний символ
    coinc = col.count('*')
    if coinc in (2, 3):                                         # шукаємо в активному рядку ** або ***
        # шукаємо рядок з відповідною кількістю співпадінь: 2 = msize-2, 3 = msize-3
        cid_col = count_coincidence_in_col(m_col, x_int, coinc)     # номер колонки, що співпадає
        if  cid_col != -1:                                          # якщо знайшли 
            m_col = fill_in_coincid_col(m_col, x_int, cid_col, coinc)   # додаємо протилежний символ, cidenc - лічильник неспівпадінь
    
    m = []
    for y in range(msize):
        col = [colum[y] for colum in m_col]
        col = ''.join(col)
        m.append(col)
    return m