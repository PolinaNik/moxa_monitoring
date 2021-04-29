# -*- coding: utf-8 -*-
###############################################
####### Скрипт для мониторинга каналов ########
###############################################

import Tkinter
import ttk
from ttk import *
import Tkinter as tk
from Tkinter import *
import tkFont
from tkdocviewer import *
import ScrolledText
import datetime
import time
from time import gmtime, strftime
from tkcalendar import Calendar
from threading import Thread
import subprocess
import os
import signal
import logging, logging.handlers
import collections
import test_config
from test_modules import delete_lines, represent_data, load_file, dump_file, play_sound

pid = os.getpid()

# Определяем количество MOXA для мониторинга из конфига
list_moxa = test_config.moxa

# selecting parameters of font
main_font = test_config.main_font
size_font = test_config.size_font
rowheight_ = test_config.rowheight

# Формирование лога
logit = logging.getLogger('logit')
handler = logging.handlers.RotatingFileHandler("%smoxa.log% test_config.folder_path", mode='a')
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logging.Formatter.converter = time.gmtime
logit.addHandler(handler)

logit.warning(str(pid))
# Создание основного окна
root = tk.Tk()
root.title("Мониторинг состояния каналов")


# Функция для просмотра лога
def insert_text():
    win = tk.Toplevel()
    win.wm_title("Просмотр лога")
    text = ScrolledText.ScrolledText(win, height=30, width=200, font=tkFont.Font(family=main_font, size=size_font))
    text.pack(expand=True, fill='both')
    with open('%smoxa.log% test_config.folder_path', 'r') as log:
        file_log = log.readlines()
        text.delete(1.0, tk.END)
        for element in file_log:
            text.insert(tk.END, element)
    but = tk.Button(win, text='Закрыть лог', command=win.destroy, activebackground='salmon',
                    font=tkFont.Font(family=main_font, size=size_font))
    but.pack()


# Вернуть канал в работу
class Popup(Menu):
    def __init__(self, master, tree, iid, num):
        Menu.__init__(self, master, tearoff=0)
        self.tree = tree
        self.num = num
        self.add_command(label="Отправить канал в ремонт до распоряжения", command=lambda: on_agreement(tree, iid, num),
                         font=tkFont.Font(family=main_font, size=size_font))
        self.add_command(label="Отправить канал в ремонт по времени", command=lambda: OnDoubleClick(tree, iid, num),
                         font=tkFont.Font(family=main_font, size=size_font))
        self.add_command(label="Выключить звук", command=lambda: make_mute(tree, iid, num),
                         font=tkFont.Font(family=main_font, size=size_font))
        #        self.add_command(label="ТЕСТ", command =comment)
        row = tree.item(iid)
        key = row["values"][0]
        remont = load_file('remont', num)
        mute = load_file('mute', num)
        self.bind("<FocusOut>", self.focusOut)
        if key in remont.keys():
            self.delete(2)
            self.delete(1)
            self.delete(0)
            self.add_command(label="Вернуть канал в работу", command=lambda: return_channel(tree, iid, num),
                             font=tkFont.Font(family=main_font, size=size_font))
        if mute[key] == 1:
            self.delete(2)
            self.delete(1)
            self.delete(0)
            self.add_command(label="Включить звук", command=lambda: make_loud(tree, iid, num),
                             font=tkFont.Font(family=main_font, size=size_font))

    def focusOut(self, event=None):
        self.unpost()


def do_popup(event, root, tree, num):
    iid = tree.identify_row(event.y)
    if iid:
        popup = Popup(root, tree, iid, num)
        try:
            tree.selection_set(iid)
            popup.tk_popup(event.x_root, event.y_root)
        finally:
            popup.grab_release()


# Функция для возвращения канала в работу
def return_channel(tree, iid, num):
    row = tree.item(iid)
    key_tree = row['values'][0]
    all_values = test_config.all_values_moxa
    name = all_values[num][0][key_tree]
    for x in all_values.keys():
        for all_dict in all_values[x][0]:
            if name == all_values[x][0][all_dict]:
                if x in list_moxa:
                    tree = all_trees[x]
                    remont = load_file('remont', x)
                    for key in remont.keys():
                        if key == key_tree:
                            del (remont[key])
                            dump_file('remont', x, remont)
                            tree_num = key_tree - 1
                            r = tree.get_children()[tree_num]
                            moxa = all_values[x][0]
                            tree.item(r, values=(str(key_tree), str(moxa[key_tree]), str('updating status...')),
                                      tags=("green",))
                            logit.warning('Канал %s в MOXA%s возвращен в работу' % (moxa[key_tree], x))


def comment():
    top = tk.Toplevel()
    top.wm_title("Info")
    frame1 = tk.Frame(top)
    frame1.pack()
    label = tk.Label(frame1, text="Комментарий или что-нибудь еще")
    label.pack()
    but = tk.Button(frame1, text="Закрыть", command=top.destroy)
    but.pack()


# Класс времени
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.hourstr = tk.StringVar(self, datetime.datetime.today().hour)
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hourstr, width=4,
                               font=tkFont.Font(family=main_font, size=size_font), state="readonly")
        self.minstr = tk.StringVar(self, datetime.datetime.today().minute)
        self.minstr.trace("w", self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minstr, width=4,
                              font=tkFont.Font(family=main_font, size=size_font), state="readonly")
        self.hour.grid()
        self.min.grid(row=0, column=1)

    def trace_var(self, *args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get()) + 1 if self.hourstr.get() != "23" else 0)
        self.last_value = self.minstr.get()


# Функция добавления канала в ремонт
def OnDoubleClick(tree, iid, num):
    row = tree.item(iid)
    key_tree = row['values'][0]
    all_values = test_config.all_values_moxa
    name = all_values[num][0][key_tree]
    top = tk.Toplevel()
    top.wm_title(name)
    frame1 = tk.Frame(top)
    frame1.pack(side=LEFT)
    frame2 = tk.Frame(top)
    frame2.pack(side=LEFT)
    frame3 = tk.Frame(top)
    frame3.pack(side=LEFT)
    lab1 = tk.Label(frame1, text='Дата и время начала работ', font=tkFont.Font(family=main_font, size=size_font))
    lab1.pack()
    cal = Calendar(frame1, font="Arial 14", selectmode="day", year=datetime.datetime.today().year,
                   month=datetime.datetime.today().month, day=datetime.datetime.today().day)
    cal.pack()
    app1 = App(frame1)
    app1.pack()
    lab2 = tk.Label(frame2, text='Дата и время завершения работ', font=tkFont.Font(family=main_font, size=size_font))
    lab2.pack()
    cal2 = Calendar(frame2, font="Arial 14", selectmode="day", year=datetime.datetime.today().year,
                    month=datetime.datetime.today().month, day=datetime.datetime.today().day)
    cal2.pack()
    app2 = App(frame2)
    app2.pack()
    but1 = tk.Button(frame3, text="Выбрать",
                     command=lambda: select(top, key_tree, name, cal.get_date(), app1.hourstr.get(), app1.minstr.get(),
                                            cal2.get_date(), app2.hourstr.get(), app2.minstr.get(), num),
                     activebackground='PaleGreen1', font=tkFont.Font(family=main_font, size=size_font), height=2,
                     width=10)
    but1.pack()
    but2 = tk.Button(frame3, text="Отмена", command=top.destroy, activebackground='salmon',
                     font=tkFont.Font(family=main_font, size=size_font), height=2, width=10)
    but2.pack()
    top.resizable(height=False, width=False)

    def select(top, key_tree, name, date1, h1, m1, date2, h2, m2, num):
        my_order = [2, 0, 1]
        # for sun 9
        #	date_list1 = date1.split('.')
        #	date_list2 = date2.split('.')
        # for sun5
        date_list1 = date1.split('/')
        date_list2 = date2.split('/')
        date_list1 = ['0' + i if len(i) == 1 else i for i in date_list1]
        date_list2 = ['0' + i if len(i) == 1 else i for i in date_list2]
        date_list1 = [date_list1[i] for i in my_order]
        date_list2 = [date_list2[i] for i in my_order]
        date_list1[0] = '20' + date_list1[0]
        date_list2[0] = '20' + date_list2[0]
        date1 = '-'.join(date_list1)
        date2 = '-'.join(date_list2)
        begin = date1 + ' ' + str(h1) + ':' + str(m1)
        end = date2 + ' ' + str(h2) + ':' + str(m2)
        d2 = {key_tree: [name, begin.encode('utf-8'), end.encode('utf-8')]}
        all_values = test_config.all_values_moxa
        par1 = "Ремонт с".decode('koi8-r').encode('koi8-r')
        par2 = "до".decode('koi8-r').encode('koi8-r')
        for x in all_values.keys():
            for all_dict in all_values[x][0]:
                if name == all_values[x][0][all_dict]:
                    if x in list_moxa:
                        tree = all_trees[x]
                        remont = load_file('remont', x)
                        remont.update(d2)
                        dump_file('remont', x, remont)
                        tree_num = key_tree - 1
                        r = tree.get_children()[tree_num]
                        tree.item(r, values=(str(key_tree), str(d2[key_tree][0]),
                                             "%s %s %s %s" % (par1, d2[key_tree][1], par2, d2[key_tree][2])),
                                  tags=("blue",))
                        logit.warning('Канал %s в MOXA%s  отправлен на ремонт на период с %s до %s' % (
                            d2[key_tree][0], num, begin.encode('utf-8'), end.encode('utf-8')))
        top.destroy()


def on_agreement(tree, iid, num):
    row = tree.item(iid)
    key_tree = row['values'][0]
    all_values = test_config.all_values_moxa
    name = all_values[num][0][key_tree]
    date_today = datetime.datetime.now()
    begin = date_today.strftime("%Y-%m-%d %H:%M")
    end = 'распоряжения'.decode('koi8-r').encode('koi8-r')
    d2 = {key_tree: [name, begin.encode('utf-8'), end]}
    all_values = test_config.all_values_moxa
    par1 = "Ремонт с".decode('koi8-r').encode('koi8-r')
    par2 = "до".decode('koi8-r').encode('koi8-r')
    for x in all_values.keys():
        for all_dict in all_values[x][0]:
            if name == all_values[x][0][all_dict]:
                if x in list_moxa:
                    tree = all_trees[x]
                    remont = load_file('remont', x)
                    remont.update(d2)
                    dump_file('remont', x, remont)
                    tree_num = key_tree - 1
                    r = tree.get_children()[tree_num]
                    tree.item(r, values=(str(key_tree), str(d2[key_tree][0]),
                                         "%s %s %s %s" % (par1, d2[key_tree][1], par2, d2[key_tree][2])),
                              tags=("blue",))
                    logit.warning('Канал %s в MOXA%s  отправлен на ремонт на период с %s до %s' % (
                        d2[key_tree][0], x, begin, end))


def make_mute(tree, iid, num):
    row = tree.item(iid)
    key_tree = row['values'][0]
    all_values = test_config.all_values_moxa
    name = all_values[num][0][key_tree]
    d2 = {key_tree: 1}
    add_in_table = test_config.all_values_moxa[num][1]
    for x in all_values.keys():
        for all_dict in all_values[x][0]:
            if name == all_values[x][0][all_dict]:
                if x in list_moxa:
                    tree = all_trees[x]
                    mute = load_file('mute', x)
                    mute.update(d2)
                    dump_file('mute', x, mute)
                    tree_num = key_tree - 1
                    r = tree.get_children()[tree_num]
                    state = 'mute' + str(add_in_table[key_tree][2])
                    tree.item(r, values=(str(add_in_table[key_tree][0]), str(add_in_table[key_tree][1]), state),
                              tags=(add_in_table[key_tree][3],))
                    logit.warning('Канал %s в MOXA%s - mute mode on' % (
                        name, x))


def make_loud(tree, iid, num):
    row = tree.item(iid)
    key_tree = row['values'][0]
    all_values = test_config.all_values_moxa
    name = all_values[num][0][key_tree]
    d2 = {key_tree: ""}
    add_in_table = test_config.all_values_moxa[num][1]
    for x in all_values.keys():
        for all_dict in all_values[x][0]:
            if name == all_values[x][0][all_dict]:
                if x in list_moxa:
                    tree = all_trees[x]
                    mute = load_file('mute', x)
                    mute.update(d2)
                    dump_file('mute', x, mute)
                    tree_num = key_tree - 1
                    r = tree.get_children()[tree_num]
                    state = str(add_in_table[key_tree][2])
                    tree.item(r, values=(
                        str(add_in_table[key_tree][0]), str(add_in_table[key_tree][1]), 'updating status...'),
                              tags=(add_in_table[key_tree][3],))
                    logit.warning('Канал %s в MOXA%s - mute mode off' % (
                        name, x))


# Формирование меню
menu_bar = tk.Menu(root)
menu_bar.add_command(label="Показать лог", command=lambda: insert_text(),
                     font=tkFont.Font(family=main_font, size=size_font))
menu_bar.add_command(label="Таблица соответствия", command=lambda: show_info(),
                     font=tkFont.Font(family=main_font, size=size_font))
menu_bar.add_command(label="Выйти из программы", command=lambda: os.kill(pid, signal.SIGKILL),
                     font=tkFont.Font(family=main_font, size=size_font))
root.config(menu=menu_bar)


# Show info
def show_info():
    top = tk.Toplevel()
    top.geometry('800x1200')
    v = DocViewer(top)
    v.pack(side="top", expand=1, fill="both")
    v.display_file("info_table.pdf")
    but = tk.Button(top, text="Закрыть", command=top.destroy, activebackground='salmon',
                    font=tkFont.Font(family=main_font, size=size_font), height=2, width=10)
    but.pack()


# Формирование раздела, в который будут помещаться таблицы
frame = tk.Frame(root)
frame.pack()

combine_font = main_font + " " + str(size_font)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background="gray18",
                fieldbackground="gray18", foreground="white", font=combine_font, rowheight=rowheight_)
style.configure("Treeview.Heading", font=combine_font)


# Функция для формирования таблицы со значениями
def make_tree(num):
    tree = ttk.Treeview(frame)
    tree["columns"] = ("one", "two", "three")
    tree.heading("#0", text="")
    tree.column("#0", minwidth=0, width=5, stretch=NO)
    tree.heading("one", text="Port")
    tree.column("one", minwidth=0, width=30, stretch=NO)
    tree.column("two", minwidth=0, width=test_config.name_column, stretch=NO)
    tree.heading("three", text="State")
    tree.column("three", minwidth=0, width=test_config.state_column, stretch=YES)
    tree['height'] = 32
    tree.tag_configure('green', background='gray7', foreground='green2')
    tree.tag_configure('red', background='gray7', foreground='tomato2')
    tree.tag_configure('blue', background='gray7', foreground='RoyalBlue')
    tree.tag_configure('yellow', background='gray7', foreground='yellow')
    tree.tag_configure('ready', background='gray7', foreground='white')
    tree.bind("<Button-3>", lambda event: do_popup(event, root, tree, num))
    tree.pack(side=LEFT)
    return tree


"""В зависимости от количества MOXA формирются таблицы.
Значение кол-ва MOXA задается в конфиге, по умолчанию 4"""

if len(list_moxa) == 4:
    tree1 = make_tree(1)
    tree2 = make_tree(2)
    tree3 = make_tree(3)
    tree4 = make_tree(4)
    all_trees = {1: tree1, 2: tree2, 3: tree3, 4: tree4}

if len(list_moxa) == 6:
    tree1 = make_tree(1)
    tree2 = make_tree(2)
    tree3 = make_tree(3)
    tree4 = make_tree(4)
    tree5 = make_tree(5)
    tree6 = make_tree(6)
    all_trees2 = {1: tree1, 2: tree2, 3: tree3, 4: tree4, 5: tree5, 6: tree6}


def insert_to_table(moxa, tree):
    for key in moxa.keys():
        tree.insert("", "end", values=(str(key), moxa[key], "<><><>"), tags=("green",))


if len(list_moxa) == 4:
    insert_to_table(test_config.all_values_moxa[1][0], tree1)
    insert_to_table(test_config.all_values_moxa[2][0], tree2)
    insert_to_table(test_config.all_values_moxa[3][0], tree3)
    insert_to_table(test_config.all_values_moxa[4][0], tree4)

if len(list_moxa) == 6:
    insert_to_table(test_config.all_values_moxa[1][0], tree1)
    insert_to_table(test_config.all_values_moxa[2][0], tree2)
    insert_to_table(test_config.all_values_moxa[3][0], tree3)
    insert_to_table(test_config.all_values_moxa[4][0], tree4)
    insert_to_table(test_config.all_values_moxa[5][0], tree5)
    insert_to_table(test_config.all_values_moxa[6][0], tree6)


def moxa_func_for_common(num, common_values, tree1, tree2):
    curenttime = datetime.datetime.today()
    name = "MOXA-%s" % num
    text = "%s %s" % (name, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    tree1.heading("two", text=text)
    tree2.heading("two", text=text)
    remember = []
    remont = load_file('remont', num)
    updatetime = load_file('updatetime', num)
    rx = load_file('rx', num)
    tx = load_file('tx', num)
    IT = load_file('IT', num)
    moxa = test_config.all_values_moxa[num][0]
    add_in_table1 = test_config.all_values_moxa[num][1]
    add_in_table2 = test_config.all_values_moxa[num + 2][1]
    mute = load_file('mute', num)
    for key in moxa.keys():
        if moxa[key] in common_values and key not in remont.keys():
            port = key + 1
            curentrx = 1
            curenttx = 1
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                dump_file('rx', num + 2, rx)
                dump_file('tx', num + 2, tx)
                if curenttx != '0' and curentrx != '0' and mute[key] == "":
                    state = '<<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                    dump_file('updatetime', num, updatetime)
                    dump_file('updatetime', num + 2, updatetime)
                if curentrx != '0' and key not in remember and mute[key] == "":
                    state = '<<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                    dump_file('updatetime', num, updatetime)
                    dump_file('updatetime', num + 2, updatetime)
                if curenttx != '0' and key not in remember and mute[key] == "":
                    state = '>>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                    dump_file('updatetime', num, updatetime)
                    dump_file('updatetime', num + 2, updatetime)
                if curenttx != '0' and curentrx != '0' and mute[key] == 1:
                    state = 'mute' + ' <<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                    dump_file('updatetime', num, updatetime)
                    dump_file('updatetime', num + 2, updatetime)
                if curentrx != '0' and key not in remember and mute[key] == 1:
                    state = 'mute' + ' <<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                    dump_file('updatetime', num, updatetime)
                    dump_file('updatetime', num + 2, updatetime)
                if curenttx != '0' and key not in remember and mute[key] == 1:
                    state = 'mute' + ' >>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                    dump_file('updatetime', num, updatetime)
                    dump_file('updatetime', num + 2, updatetime)
            IT[key] = curenttime - updatetime[key]
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and moxa[
                key] != "" and mute[key] == "":
                dump_file('updatetime', num, updatetime)
                dump_file('updatetime', num + 2, updatetime)
                absent = represent_data(str(IT[key]))
                state = str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table1.update(d)
                add_in_table2.update(d)
            if IT[key] > datetime.timedelta(hours=12) and moxa[key] != "" and mute[key] == "":
                absent = represent_data(str(IT[key]))
                state = str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table1.update(d)
                add_in_table2.update(d)
            if moxa[key] == "":
                lst = [key, "", "", 'green']
                d = {key: lst}
                add_in_table1.update(d)
                add_in_table2.update(d)
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and moxa[
                key] != "" and mute[key] == 1:
                dump_file('updatetime', num, updatetime)
                dump_file('updatetime', num + 2, updatetime)
                absent = represent_data(str(IT[key]))
                state = 'mute' + ' ' + str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table1.update(d)
                add_in_table2.update(d)
            if IT[key] > datetime.timedelta(hours=12) and moxa[key] != "" and mute[key] == 1:
                absent = represent_data(str(IT[key]))
                state = 'mute' + ' ' + str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table1.update(d)
                add_in_table2.update(d)
                # Условие для всех каналов, кроме РЛИ_для_ВЕГА (при пропадании более чем на 2 мин загорается красным)
            if datetime.timedelta(minutes=test_config.signalisation) < IT[key] < datetime.timedelta(
                    minutes=test_config.signalisation + 1) and moxa[key] != "" and moxa[
                key] != "Объединенная РЛИ для ВЕГА" and mute[key] != 1:
                logit.warning('%s - %s пропал. Время пропадания - %s' % (
                    name, moxa[key], updatetime[key].replace(microsecond=0)))
                play_sound()

    for key in remont.keys():
        if remont[key][0] in common_values:
            port = key + 1
            rem = remont[key]
            name_rem = rem[0]
            par1 = "Ремонт с ".decode('koi8-r').encode('koi8-r')
            par2 = " до ".decode('koi8-r').encode('koi8-r')
            period = par1 + rem[1] + par2 + rem[2]
            period2 = 'mute ' + par1 + rem[1] + par2 + rem[2]
            lst = [key, name_rem, period, 'blue']
            d = {key: lst}
            add_in_table1.update(d)
            add_in_table2.update(d)
            curentrx = 1
            curenttx = 1
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                if curenttx != '0' and curentrx != '0' and mute[key] == "":
                    lst = [key, name_rem, period, 'ready']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                elif curentrx != '0' and key not in remember and mute[key] == "":
                    lst = [key, name_rem, period, 'ready']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                elif curenttx != '0' and key not in remember and mute[key] == "":
                    lst = [key, name_rem, period, 'ready']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                if curenttx != '0' and curentrx != '0' and mute[key] == 1:
                    lst = [key, name_rem, period2, 'ready']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                elif curentrx != '0' and key not in remember and mute[key] == 1:
                    lst = [key, name_rem, period2, 'ready']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
                elif curenttx != '0' and key not in remember and mute[key] == 1:
                    lst = [key, name_rem, period2, 'ready']
                    d = {key: lst}
                    add_in_table1.update(d)
                    add_in_table2.update(d)
    add_in_table1 = collections.OrderedDict(sorted(add_in_table1.items()))
    add_in_table2 = collections.OrderedDict(sorted(add_in_table2.items()))
    for key in add_in_table1.keys():
        num = key - 1
        r = tree1.get_children()[num]
        tree1.item(r, values=(str(add_in_table1[key][0]), str(add_in_table1[key][1]), str(add_in_table1[key][2])),
                  tags=(add_in_table1[key][3],))
    for key in add_in_table2.keys():
        num = key - 1
        r = tree2.get_children()[num]
        tree2.item(r, values=(str(add_in_table2[key][0]), str(add_in_table2[key][1]), str(add_in_table2[key][2])),
                  tags=(add_in_table2[key][3],))


def moxa_func_for_unique(num, unique_values, tree):
    curenttime = datetime.datetime.today()
    name = "MOXA-%s" % num
    text = "%s %s" % (name, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    tree.heading("two", text=text)
    remember = []
    remont = load_file('remont', num)
    updatetime = load_file('updatetime', num)
    rx = load_file('rx', num)
    tx = load_file('tx', num)
    IT = load_file('IT', num)
    moxa = test_config.all_values_moxa[num][0]
    add_in_table = test_config.all_values_moxa[num][1]
    mute = load_file('mute', num)
    for key in moxa.keys():
        if moxa[key] in unique_values and key not in remont.keys():
            port = key + 1
            curentrx = 1
            curenttx = 1
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                if curenttx != '0' and curentrx != '0' and mute[key] == "":
                    state = '<<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curentrx != '0' and key not in remember and mute[key] == "":
                    state = '<<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and key not in remember and mute[key] == "":
                    state = '>>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and curentrx != '0' and mute[key] == 1:
                    state = 'mute' + ' <<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curentrx != '0' and key not in remember and mute[key] == 1:
                    state = 'mute' + ' <<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and key not in remember and mute[key] == 1:
                    state = 'mute' + ' >>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
            IT[key] = curenttime - updatetime[key]
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and moxa[
                key] != "" and mute[key] == "":
                dump_file('updatetime', num, updatetime)
                absent = represent_data(str(IT[key]))
                state = str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(hours=12) and moxa[key] != "" and mute[key] == "":
                absent = represent_data(str(IT[key]))
                state = str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table.update(d)
            if moxa[key] == "":
                lst = [key, "", "", 'green']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and moxa[
                key] != "" and mute[key] == 1:
                dump_file('updatetime', num, updatetime)
                absent = represent_data(str(IT[key]))
                state = 'mute' + ' ' + str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(hours=12) and moxa[key] != "" and mute[key] == 1:
                absent = represent_data(str(IT[key]))
                state = 'mute' + ' ' + str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table.update(d)
                # Условие для всех каналов, кроме РЛИ_для_ВЕГА (при пропадании более чем на 2 мин загорается красным)
            if datetime.timedelta(minutes=test_config.signalisation) < IT[key] < datetime.timedelta(
                    minutes=test_config.signalisation + 1) and moxa[key] != "" and moxa[
                key] != "Объединенная РЛИ для ВЕГА" and mute[key] != 1:
                logit.warning('%s - %s пропал. Время пропадания - %s' % (
                    name, moxa[key], updatetime[key].replace(microsecond=0)))
                play_sound()

    for key in remont.keys():
        if remont[key][0] in unique_values:
            port = key + 1
            rem = remont[key]
            name_rem = rem[0]
            par1 = "Ремонт с ".decode('koi8-r').encode('koi8-r')
            par2 = " до ".decode('koi8-r').encode('koi8-r')
            period = par1 + rem[1] + par2 + rem[2]
            period2 = 'mute ' + par1 + rem[1] + par2 + rem[2]
            lst = [key, name_rem, period, 'blue']
            d = {key: lst}
            add_in_table.update(d)
            curentrx = 1
            curenttx = 1
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                if curenttx != '0' and curentrx != '0' and mute[key] == "":
                    lst = [key, name_rem, period, 'ready']
                    d = {key: lst}
                    add_in_table.update(d)
                elif curentrx != '0' and key not in remember and mute[key] == "":
                    lst = [key, name_rem, period, 'ready']
                    d = {key: lst}
                    add_in_table.update(d)
                elif curenttx != '0' and key not in remember and mute[key] == "":
                    lst = [key, name_rem, period, 'ready']
                    d = {key: lst}
                    add_in_table.update(d)
                if curenttx != '0' and curentrx != '0' and mute[key] == 1:
                    lst = [key, name_rem, period2, 'ready']
                    d = {key: lst}
                    add_in_table.update(d)
                elif curentrx != '0' and key not in remember and mute[key] == 1:
                    lst = [key, name_rem, period2, 'ready']
                    d = {key: lst}
                    add_in_table.update(d)
                elif curenttx != '0' and key not in remember and mute[key] == 1:
                    lst = [key, name_rem, period2, 'ready']
                    d = {key: lst}
                    add_in_table.update(d)
    add_in_table = collections.OrderedDict(sorted(add_in_table.items()))
    for key in add_in_table.keys():
        num = key - 1
        r = tree.get_children()[num]
        tree.item(r, values=(str(add_in_table[key][0]), str(add_in_table[key][1]), str(add_in_table[key][2])),
                  tags=(add_in_table[key][3],))


def moxa_func(tree, num):
    curenttime = datetime.datetime.today()
    name = "MOXA-%s" % num
    text = "%s %s" % (name, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    tree.heading("two", text=text)
    remember = []
    remont = load_file('remont', num)
    updatetime = load_file('updatetime', num)
    rx = load_file('rx', num)
    tx = load_file('tx', num)
    IT = load_file('IT', num)
    moxa = test_config.all_values_moxa[num][0]
    ip = test_config.all_values_moxa[num][2]
    add_in_table = test_config.all_values_moxa[num][1]
    mute = load_file('mute', num)
    for key in moxa.keys():
        if key not in remont.keys():
            port = key + 1
            curentrx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip,
                                                '.1.3.6.1.2.1.2.2.1.10.%s' % port]).rstrip()
            curenttx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip,
                                                '.1.3.6.1.2.1.2.2.1.16.%s' % port]).rstrip()
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                if curenttx != '0' and curentrx != '0' and mute[key] == "":
                    state = '<<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curentrx != '0' and key not in remember and mute[key] == "":
                    state = '<<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and key not in remember and mute[key] == "":
                    state = '>>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and curentrx != '0' and mute[key] == 1:
                    state = 'mute' + ' <<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curentrx != '0' and key not in remember and mute[key] == 1:
                    state = 'mute' + ' <<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and key not in remember and mute[key] == 1:
                    state = 'mute' + ' >>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
            IT[key] = curenttime - updatetime[key]
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and moxa[
                key] != "" and mute[key] == "":
                dump_file('updatetime', num, updatetime)
                absent = represent_data(str(IT[key]))
                state = str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(hours=12) and moxa[key] != "" and mute[key] == "":
                absent = represent_data(str(IT[key]))
                state = str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table.update(d)
            if moxa[key] == "":
                lst = [key, "", "", 'green']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and moxa[
                key] != "" and mute[key] == 1:
                dump_file('updatetime', num, updatetime)
                absent = represent_data(str(IT[key]))
                state = 'mute' + ' ' + str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(hours=12) and moxa[key] != "" and mute[key] == 1:
                absent = represent_data(str(IT[key]))
                state = 'mute' + ' ' + str(updatetime[key]).split(".")[0] + ' ' + absent
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table.update(d)
                # Условие для всех каналов, кроме РЛИ_для_ВЕГА (при пропадании более чем на 2 мин загорается красным)
            if datetime.timedelta(minutes=test_config.signalisation) < IT[key] < datetime.timedelta(
                    minutes=test_config.signalisation + 1) and moxa[key] != "" and moxa[
                key] != "Объединенная РЛИ для ВЕГА" and mute[key] != 1:
                logit.warning('%s - %s пропал. Время пропадания - %s' % (
                    name, moxa[key], updatetime[key].replace(microsecond=0)))
                os.system('/opt/csw/bin/mpg123 /sintez/sintez/moxa_monitoring/sound.mp3')

    for key in remont.keys():
        port = key + 1
        rem = remont[key]
        name_rem = rem[0]
        par1 = "Ремонт с ".decode('koi8-r').encode('koi8-r')
        par2 = " до ".decode('koi8-r').encode('koi8-r')
        period = par1 + rem[1] + par2 + rem[2]
        period2 = 'mute ' + par1 + rem[1] + par2 + rem[2]
        lst = [key, name_rem, period, 'blue']
        d = {key: lst}
        add_in_table.update(d)
        curentrx = subprocess.check_output(
            ['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip, '.1.3.6.1.2.1.2.2.1.10.%s' % port]).rstrip()
        curenttx = subprocess.check_output(
            ['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip, '.1.3.6.1.2.1.2.2.1.16.%s' % port]).rstrip()
        if curentrx != rx[key] or curenttx != tx[key]:
            updatetime[key] = curenttime
            rx[key] = curentrx
            tx[key] = curenttx
            dump_file('rx', num, rx)
            dump_file('tx', num, tx)
            if curenttx != '0' and curentrx != '0' and mute[key] == "":
                lst = [key, name_rem, period, 'ready']
                d = {key: lst}
                add_in_table.update(d)
            elif curentrx != '0' and key not in remember and mute[key] == "":
                lst = [key, name_rem, period, 'ready']
                d = {key: lst}
                add_in_table.update(d)
            elif curenttx != '0' and key not in remember and mute[key] == "":
                lst = [key, name_rem, period, 'ready']
                d = {key: lst}
                add_in_table.update(d)
            if curenttx != '0' and curentrx != '0' and mute[key] == 1:
                lst = [key, name_rem, period2, 'ready']
                d = {key: lst}
                add_in_table.update(d)
            elif curentrx != '0' and key not in remember and mute[key] == 1:
                lst = [key, name_rem, period2, 'ready']
                d = {key: lst}
                add_in_table.update(d)
            elif curenttx != '0' and key not in remember and mute[key] == 1:
                lst = [key, name_rem, period2, 'ready']
                d = {key: lst}
                add_in_table.update(d)
    add_in_table = collections.OrderedDict(sorted(add_in_table.items()))
    for key in add_in_table.keys():
        num = key - 1
        r = tree.get_children()[num]
        tree.item(r, values=(str(add_in_table[key][0]), str(add_in_table[key][1]), str(add_in_table[key][2])),
                  tags=(add_in_table[key][3],))


# Функция запуска бесконечного цикла мониторинга
def update_tables1(num):
    while True:
        count = 0
        rx = load_file('rx', num)
        for key in rx.keys():
            if key != 1:
                new = {key: count}
                rx.update(new)
                dump_file('rx', num, rx)
        count += 1
        time.sleep(20)


def update_tables2(num):
    while True:
        count = 0
        rx = load_file('rx', num)
        for key in rx.keys():
            if key != 1:
                new = {key: count}
                rx.update(new)
                dump_file('rx', num, rx)
        count += 1
        time.sleep(20)


def common_function(num, common_values, tree1, tree2):
    while True:
        try:
            moxa_func_for_common(num, common_values, tree1, tree2)
            time.sleep(test_config.time1)
        except:
            pass


def unique_function(num, unique_values, tree):
    while True:
        try:
            moxa_func_for_unique(num, unique_values, tree)
            time.sleep(test_config.time1)
        except:
            pass


# Deleting log
def start_function2():
    while True:
        try:
            delete_lines()
            time.sleep(test_config.time2)
        except:
            pass


# Запуск параллельных потоков
if len(list_moxa) == 4:
    x1 = Thread(target=common_function, args=(1, test_config.common_values1, tree1, tree3))
    x1.start()

    x2 = Thread(target=common_function, args=(2, test_config.common_values2, tree2, tree4))
    x2.start()

    x3 = Thread(target=update_tables1, args=(1,))
    x3.start()

    x4 = Thread(target=update_tables1, args=(3,))
    x4.start()

    x5 = Thread(target=update_tables2, args=(2,))
    x5.start()

    x6 = Thread(target=update_tables2, args=(4,))
    x6.start()

    x7 = Thread(target=start_function2)
    x7.start()

    x8 = Thread(target=unique_function, args=(1, test_config.unique_values1, tree1))
    x8.start()

    x9 = Thread(target=unique_function, args=(2, test_config.unique_values2, tree2))
    x9.start()

    x10 = Thread(target=unique_function, args=(3, test_config.unique_values1, tree3))
    x10.start()

    x11 = Thread(target=unique_function, args=(4, test_config.unique_values2, tree4))
    x11.start()


def start_function(tree, num):
    while True:
        try:
            moxa_func(tree, num)
            time.sleep(test_config.time1)
        except:
            pass


if len(list_moxa) == 6:
    x1 = Thread(target=start_function, args=(tree1, 1,))
    x1.start()

    x2 = Thread(target=start_function, args=(tree2, 2,))
    x2.start()

    x3 = Thread(target=start_function, args=(tree3, 3,))
    x3.start()

    x4 = Thread(target=start_function, args=(tree4, 4,))
    x4.start()

    x5 = Thread(target=start_function, args=(tree5, 5,))
    x5.start()

    x6 = Thread(target=start_function, args=(tree6, 6,))
    x6.start()

    # x7 = Thread(target=start_function2)
    # x7.start()

root.resizable(height=False, width=False)
root.mainloop()
