#-*- coding: utf-8 -*-

###############################################
####### Конфиг для мониторинга каналов #########
###############################################

"""Ниже в квадратных скобках укажите номера MOXA,
которые нужно мониторить"""

moxa = [1,2,3,4]

#Выберите шрифт
main_font = "Helvetica"

#Размер шрифта
size_font = 11

#Высота строки
rowheight = 18

#Размер колонок
name_column = 230
state_column = 280

#IP-адреса MOXA
ip1 = 'moxa1'
ip2 = 'moxa2'
ip3 = 'moxa3'
ip4 = 'moxa4'
ip5 = 'moxa1'
ip6 = 'moxa2'

import datetime

moxa1 = {1: "ОРЛ-Т Комсомольск-1",
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
         29: "Объединенная РЛИ для ГЦ Москва ",
         30: "Объединенная РЛИ для МС КПТС",
         31: "Метеосервер",
         32: "Объединенная РЛИ для ВЕГА"}

moxa2 = {1: "ОРЛ-Т Комсомольск-2",
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

moxa3 = {1: "ОРЛ-Т Комсомольск-1",
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

moxa4 = {1: "ОРЛ-Т Комсомольск-2",
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



rx1 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

rx2 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

rx3 =  {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}
      
rx4 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

rx5 ={1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

rx6 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

tx1 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

tx2 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

tx3 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}
      
tx4 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

tx5 = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

tx6 ={1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",
          10: "", 11: "", 12: "", 13: "", 14:"", 15: "", 16:"", 17: "", 
          18: "",19: "", 20: "", 21: "", 22: "", 23:"", 24: "", 25:"",
           26: "", 27: "",28: "", 29: "", 30: "", 31: "", 32:""}

updatetime1 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(), 18:datetime.datetime.today(), 19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

updatetime2 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

updatetime3 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

updatetime4 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

updatetime5 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

updatetime6 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

IT1 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

IT2 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}
      
IT3 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

IT4 = {1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

IT5 ={1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}
IT6 ={1: datetime.datetime.today(),2: datetime.datetime.today(),
      3:datetime.datetime.today(), 4: datetime.datetime.today(),
      5:datetime.datetime.today(), 6: datetime.datetime.today(),
      7:datetime.datetime.today(), 8: datetime.datetime.today(),
      9: datetime.datetime.today(), 10:datetime.datetime.today(),
      11: datetime.datetime.today(), 12:datetime.datetime.today(),
      13: datetime.datetime.today(), 14:datetime.datetime.today(),
      15: datetime.datetime.today(), 16:datetime.datetime.today(), 
      17: datetime.datetime.today(),18:datetime.datetime.today(),19:datetime.datetime.today(), 
      20: datetime.datetime.today(),21:datetime.datetime.today(), 
      22: datetime.datetime.today(),23:datetime.datetime.today(), 
      24: datetime.datetime.today(), 25: datetime.datetime.today(), 
      26:datetime.datetime.today(), 27: datetime.datetime.today(),
      28:datetime.datetime.today(), 29: datetime.datetime.today(), 
      30:datetime.datetime.today(), 31: datetime.datetime.today(), 32:datetime.datetime.today()}

remont1 = {}
remont2 = {}
remont3 = {}
remont4 = {}
remont5 = {}
remont6 = {}

add_in_table1 = {}
add_in_table2 = {}
add_in_table3 = {}
add_in_table4 = {}
add_in_table5 = {}
add_in_table6 = {}

all_values_moxa = {
    1: [moxa1, rx1, tx1, updatetime1, IT1, remont1, add_in_table1, 'moxa1'],
    2: [moxa2, rx2, tx2, updatetime2, IT2, remont2, add_in_table2, 'moxa2'],
    3: [moxa3, rx3, tx3, updatetime3, IT3, remont3, add_in_table3, 'moxa3'],
    4: [moxa4, rx4, tx4, updatetime4, IT4, remont4, add_in_table4, 'moxa4'],
    5: [moxa5, rx5, tx5, updatetime5, IT5, remont5, add_in_table5,  'moxa1'],
    6: [moxa6, rx6, tx6, updatetime6, IT6, remont6, add_in_table6, 'moxa2']

}


