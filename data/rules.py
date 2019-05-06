import data.row
import data.column
import data.check
''' алгоритм обробки рядочків і колонок на однозначні рішення'''

def through_the_rules(M, msize, max_digit):
    if not(data.check.everything_ok(M, msize, max_digit)):
        return M
    for x in range(msize):    # ітератор рядочків/колонок
        # Робота з рядочками
        M = data.row.fill_in_row_by_1or0(M, msize, max_digit, x) # якщо всі 0/1 вже стоять, то заповнити вільні місц 1/0
        M = data.row.fill_in_row_by_010or101(M, x)               # Заповнює проміжки 0*0/1*1 відповідно 1/0
        M = data.row.fill_in_row_by_0110or1001(M, x)             # заповнюються очевидні комбінації *00* та *11*
        M = data.row.fill_1_in_0xxx10(M, msize, max_digit, x)    # заповнення 3го вільного місця, бо 3 підряд стояти не можуть,
        M = data.row.fill_0_in_1xxx01(M, msize, max_digit, x)    # приклад 0***10 має єдине, очевидне вирішення - 01**10
        M = data.row.coincidence_in_row(M, msize, x)             # у рядку з **/*** дати протилежний символ проти такого самого заповненого рядка
        # Робота з колонками
        M = data.column.fill_in_col_by_1or0(M, msize, max_digit, x)
        M = data.column.fill_in_col_by_010or101(M, x)
        M = data.column.fill_in_col_by_0110or1001(M, x)
        M = data.column.fill_in_col_0xxx10(M, msize, max_digit, x)
        M = data.column.fill_in_col_1xxx01(M, msize, max_digit, x)
        M = data.column.coincidence_in_col(M, msize, x)        
    return M