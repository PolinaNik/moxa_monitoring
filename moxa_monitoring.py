# -*- coding: utf-8 -*-

""" Главное окно приложения """

import ttk
import Tkinter as tk
import tkFont
import time
import os
import signal
import logging.handlers
from functools import partial
from threading import Thread

from config import all_values_moxa, moxa as list_moxa
from config import main_font, size_font, rowheight as rowheight_
from modules import insert_text, show_info
from modules import Tree, do_popup, do_popup2
from modules import check, clean_log

# Определяем ID процесса
pid = os.getpid()

# Выбираются номера MOXA, которые заложены в list_moxa в конфиге
all_values = {key: all_values_moxa[key] for key in all_values_moxa if key in list_moxa}

############# Формирование лога ######################
logit = logging.getLogger('logit')
handler = logging.handlers.RotatingFileHandler("moxa.log", mode='a')
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logging.Formatter.converter = time.gmtime
logit.addHandler(handler)

################## Создание основного окна ##################
root = tk.Tk()
root.title("Мониторинг состояния каналов")

frame = tk.Frame(root)
frame.pack()

################## Меню приложения ##################
menu_bar = tk.Menu(root)
menu_bar.add_command(label="Показать лог", command=lambda: insert_text(),
                     font=tkFont.Font(family=main_font, size=size_font))
menu_bar.add_command(label="Таблица соответствия", command=lambda: show_info(),
                     font=tkFont.Font(family=main_font, size=size_font))
menu_bar.add_command(label="Выйти из программы", command=lambda: os.kill(pid, signal.SIGKILL),
                     font=tkFont.Font(family=main_font, size=size_font))
root.config(menu=menu_bar)

################## Стиль таблицы ##################
combine_font = main_font + " " + str(size_font)
style = ttk.Style(frame)
style.theme_use("clam")
style.configure("style1.Treeview", background="gray18",
                fieldbackground="gray18", foreground="white", font=combine_font, rowheight=rowheight_)
style.configure("style1.Treeview.Heading", font=combine_font)

style.configure("style2.Treeview", background="gray18",
                fieldbackground="gray18", foreground="white", font=combine_font, rowheight=rowheight_)
style.configure("style2.Treeview.Heading", font=combine_font)

style.configure("style3.Treeview", background="gray18",
                fieldbackground="gray18", foreground="white", font=combine_font, rowheight=rowheight_)
style.configure("style3.Treeview.Heading", font=combine_font)

style.configure("style4.Treeview", background="blue",
                fieldbackground="blue", foreground="white", font=combine_font, rowheight=rowheight_)
style.configure("style4.Treeview.Heading", font=combine_font)

list_styles_names = {1: "style1.Treeview", 2: "style2.Treeview", 3: "style3.Treeview", 4: "style4.Treeview"}

################## Формирование таблиц ##################
working_trees = {num: Tree(root, frame, num, logit, all_values, list_styles_names) for num in list_moxa}
for key in working_trees.keys():
    tree = working_trees[key]
    tree.tree.bind("<Button-3>",
                   partial(do_popup, root=root, num=key, all_trees=working_trees, logit=logit, style=style))
    tree.tree.bind("<1>", partial(do_popup2, num=key, style=style))

################## Создание потоков ####################

thread_list = []

for num in working_trees.keys():
    thread_tree = Thread(target=check, args=(num, logit, working_trees))
    thread_list.append(thread_tree)

thread_log = Thread(target=clean_log)
thread_list.append(thread_log)

# for thread in thread_list:
#     thread.start()

root.mainloop()
