# -*- coding: utf-8 -*-

###############################################
####### Конфиг для мониторинга каналов #########
###############################################

"""Ниже в квадратных скобках укажите номера MOXA,
которые нужно мониторить"""

moxa = [1, 2, 3, 4]

# Выберите шрифт
main_font = "Helvetica"

# Размер шрифта
size_font = 11

# Высота строки
rowheight = 18

# Размер колонок
name_column = 230
state_column = 280

# IP-адреса MOXA
ip1 = 'moxa1'
ip2 = 'moxa2'
ip3 = 'moxa3'
ip4 = 'moxa4'
ip5 = 'moxa1'
ip6 = 'moxa2'

# Время, через которое появится звуковая сигнализация при отсутствии канала (мин)
signalisation = 2

# Время обновления сканирования MOXA в секундах
time_update = 50
# Время сканирования и зачистки старых строк в логе (старше 30 дней) в секундах
time_clean_log = 3600

moxa1 = {1: "ОРЛ-Т Комсомольск (Сопка)-1",
         2: "ОРЛ-Т Хабаровск (МВРЛ)-1",
         3: "",
         4: "ОРЛ-Т Дальнереченск-1",
         5: "ОРЛ-Т Светлая-1",
         6: "ОРЛ-Т Советская Гавань-1",
         7: "ОРЛ-Т Архара-1",
         8: "ОРЛ-Т Экимчан (ПРЛ)-1",
         9: "ОРЛ-Т Благовещенск-1",
         10: "ОРЛ-Т Магдагачи-1",
         11: "ОРЛ-Т Кавалерово-1",
         12: "ОРЛ-Т Черный Куст-1",
         13: "ОРЛ-Т Южно-Сахалинск-1",
         14: "ОРЛ-Т Николаевск-на-Амуре-1",
         15: "ОРЛ-Т Оха-1",
         16: "ОРЛ-Т Охотск-1",
         17: "ОРЛ-Т Экимчан (ВРЛ)-1",
         18: "",
         19: "АРП Оха",
         20: "АРП Архара",
         21: "АРП Магдагачи",
         22: "АРП Благовещенск",
         23: "АРП Южно-Сахалинск",
         24: "АРП Владивосток",
         25: "ОРЛ-Т Магадан (Крона)",
         26: "ОРЛ-Т Хабаровск (Сопка)-1",
         27: "ОРЛ-А Хабаровск (Лира-А10)-1",
         28: "ОРЛ-А Владивосток (Кневичи)",
         29: "Объединенная РЛИ для ГЦ Москва ",
         30: "Объединенная РЛИ для МС КПТС",
         31: "Метеосервер",
         32: "Объединенная РЛИ для ВЕГА"}

moxa2 = {1: "ОРЛ-Т Комсомольск (Сопка)-2",
         2: "ОРЛ-Т Хабаровск (МВРЛ)-2",
         3: "",
         4: "ОРЛ-Т Дальнереченск-2",
         5: "ОРЛ-Т Светлая-2",
         6: "ОРЛ-Т Советская Гавань-2",
         7: "ОРЛ-Т Архара-2",
         8: "ОРЛ-Т Экимчан (ПРЛ)-2",
         9: "ОРЛ-Т Благовещенск-2",
         10: "ОРЛ-Т Магдагачи-2",
         11: "ОРЛ-Т Кавалерово-2",
         12: "ОРЛ-Т Черный Куст-2",
         13: "ОРЛ-Т Южно-Сахалинск-2",
         14: "ОРЛ-Т Николаевск-на-Амуре-2",
         15: "ОРЛ-Т Оха-2",
         16: "ОРЛ-Т Охотск-2",
         17: "ОРЛ-Т Экимчан (ВРЛ)-2",
         18: "",
         19: "ОРЛ-Т Усть-Большерецк",
         20: "ОРЛ-Т Теплый Ключ (НЕ РАСПОЗН.)",
         21: "ОРЛ-А Благовещенск",
         22: "ОРЛ-А Итуруп",
         23: "ОРЛ-А Южно-Сахалинск",
         24: "АРП Экимчан",
         25: "ОРЛ-А Охотск (Резерв ОРЛ-Т Охотск)",
         26: "ОРЛ-Т Хабаровск (Сопка)-2",
         27: "ОРЛ-А Хабаровск (Лира-А10)-2",
         28: "АРП Хабаровск",
         29: "АРП Дальнереченск",
         30: "АРП П.Осипенко",
         31: "АРП Комсомольск",
         32: "Объединенная РЛИ для ФСО"}

moxa3 = {1: "ОРЛ-Т Комсомольск (Сопка)-1",
         2: "ОРЛ-Т Хабаровск (МВРЛ)-1",
         3: "",
         4: "ОРЛ-Т Дальнереченск-1",
         5: "ОРЛ-Т Светлая-1",
         6: "ОРЛ-Т Советская Гавань-1",
         7: "ОРЛ-Т Архара-1",
         8: "ОРЛ-Т Экимчан (ПРЛ)-1",
         9: "ОРЛ-Т Благовещенск-1",
         10: "ОРЛ-Т Магдагачи-1",
         11: "ОРЛ-Т Кавалерово-1",
         12: "ОРЛ-Т Черный Куст-1",
         13: "ОРЛ-Т Южно-Сахалинск-1",
         14: "ОРЛ-Т Николаевск-на-Амуре-1",
         15: "ОРЛ-Т Оха-1",
         16: "ОРЛ-Т Охотск-1",
         17: "ОРЛ-Т Экимчан (ВРЛ)-1",
         18: "",
         19: "АРП Оха",
         20: "АРП Архара",
         21: "АРП Магдагачи",
         22: "АРП Благовещенск",
         23: "АРП Южно-Сахалинск",
         24: "АРП Владивосток",
         25: "ОРЛ-Т Магадан (Крона)",
         26: "ОРЛ-Т Хабаровск (Сопка)-1",
         27: "ОРЛ-А Хабаровск (Лира-А10)-1",
         28: "ОРЛ-А Владивосток (Кневичи)",
         29: "ОРЛ-Т Усть-Мая",
         30: "Объединенная РЛИ для МС КПТС",
         31: "ОРЛ-А Николаевск (резерв ОРЛ-Т)",
         32: ""}

moxa4 = {1: "ОРЛ-Т Комсомольск (Сопка)-2",
         2: "ОРЛ-Т Хабаровск (МВРЛ)-2",
         3: "",
         4: "ОРЛ-Т Дальнереченск-2",
         5: "ОРЛ-Т Светлая-2",
         6: "ОРЛ-Т Советская Гавань-2",
         7: "ОРЛ-Т Архара-2",
         8: "ОРЛ-Т Экимчан (ПРЛ)-2",
         9: "ОРЛ-Т Благовещенск-2",
         10: "ОРЛ-Т Магдагачи-2",
         11: "ОРЛ-Т Кавалерово-2",
         12: "ОРЛ-Т Черный Куст-2",
         13: "ОРЛ-Т Южно-Сахалинск-2",
         14: "ОРЛ-Т Николаевск-на-Амуре-2",
         15: "ОРЛ-Т Оха-2",
         16: "ОРЛ-Т Охотск-2",
         17: "ОРЛ-Т Экимчан (ВРЛ)-2",
         18: "",
         19: "ОРЛ-Т Усть-Большерецк",
         20: "ОРЛ-Т Теплый Ключ (НЕ РАСПОЗН.)",
         21: "ОРЛ-А Благовещенск",
         22: "ОРЛ-А Итуруп",
         23: "ОРЛ-А Южно-Сахалинск",
         24: "АРП Экимчан",
         25: "ОРЛ-А Охотск (Резерв ОРЛ-Т Охотск)",
         26: "ОРЛ-Т Хабаровск (Сопка)-2",
         27: "ОРЛ-А Хабаровск (Лира-А10)-2",
         28: "АРП Хабаровск",
         29: "АРП Дальнереченск",
         30: "АРП П.Осипенко",
         31: "АРП Комсомольск",
         32: "Объединенная РЛИ для Дуб-2"}

moxa5 = {1: "ОРЛ-Т Комсомольск-1",
         2: "ОРЛ-Т Хабаровск (МВРЛ)-1",
         3: "",
         4: "ОРЛ-Т Дальнереченск-1",
         5: "ОРЛ-Т Светлая-1",
         6: "ОРЛ-Т Советская Гавань-1",
         7: "ОРЛ-Т Архара-1",
         8: "ОРЛ-Т Экимчан (ПРЛ)-1",
         9: "ОРЛ-Т Благовещенск-1",
         10: "ОРЛ-Т Магдагачи-1",
         11: "ОРЛ-Т Кавалерово-1",
         12: "ОРЛ-Т Черный Куст-1",
         13: "ОРЛ-Т Южно-Сахалинск-1",
         14: "ОРЛ-Т Николаевск-на-Амуре-1",
         15: "ОРЛ-Т Оха-1",
         16: "ОРЛ-Т Охотск-1",
         17: "ОРЛ-Т Экимчан (ВРЛ)-1",
         18: "",
         19: "АРП Оха",
         20: "АРП Архара",
         21: "АРП Магдагачи",
         22: "АРП Благовещенск",
         23: "АРП Южно-Сахалинск",
         24: "АРП Владивосток",
         25: "Объединенная РЛИ из Магадана",
         26: "ОРЛ-Т Хабаровск (Сопка)-1",
         27: "ОРЛ-А Хабаровск (Лира-А10)-1",
         28: "ОРЛ-А Владивосток (Кневичи)",
         29: "ОРЛ-Т Усть-Мая",
         30: "Объединенная РЛИ для МС КПТС",
         31: "ОРЛ-А Николаевск (резерв ОРЛ-Т)",
         32: ""}

moxa6 = {1: "ОРЛ-Т Комсомольск-2",
         2: "ОРЛ-Т Хабаровск (МВРЛ)-2",
         3: "",
         4: "ОРЛ-Т Дальнереченск-2",
         5: "ОРЛ-Т Светлая-2",
         6: "ОРЛ-Т Советская Гавань-2",
         7: "ОРЛ-Т Архара-2",
         8: "ОРЛ-Т Экимчан (ПРЛ)-2",
         9: "ОРЛ-Т Благовещенск-2",
         10: "ОРЛ-Т Магдагачи-2",
         11: "ОРЛ-Т Кавалерово-2",
         12: "ОРЛ-Т Черный Куст-2",
         13: "ОРЛ-Т Южно-Сахалинск-2",
         14: "ОРЛ-Т Николаевск-на-Амуре-2",
         15: "ОРЛ-Т Оха-2",
         16: "ОРЛ-Т Охотск-2",
         17: "ОРЛ-Т Экимчан (ВРЛ)-2",
         18: "",
         19: "ОРЛ-Т Усть-Большерецк",
         20: "ОРЛ-Т Теплый Ключ (НЕ РАСПОЗН.)",
         21: "ОРЛ-А Благовещенск",
         22: "ОРЛ-А Итуруп",
         23: "ОРЛ-А Южно-Сахалинск",
         24: "АРП Экимчан",
         25: "ОРЛ-А Охотск (Резерв ОРЛ-Т Охотск)",
         26: "ОРЛ-Т Хабаровск (Сопка)-2",
         27: "ОРЛ-А Хабаровск (Лира-А10)-2",
         28: "АРП Хабаровск",
         29: "АРП Дальнереченск",
         30: "АРП П.Осипенко",
         31: "АРП Комсомольск",
         32: "Объединенная РЛИ для Дуб-2"}

add_in_table1 = {}
add_in_table2 = {}
add_in_table3 = {}
add_in_table4 = {}
add_in_table5 = {}
add_in_table6 = {}

all_values_moxa = {
    1: [moxa1, add_in_table1, ip1],
    2: [moxa2, add_in_table2, ip2],
    3: [moxa3, add_in_table3, ip3],
    4: [moxa4, add_in_table4, ip4],
    5: [moxa5, add_in_table5, ip5],
    6: [moxa6, add_in_table6, ip6]

}
