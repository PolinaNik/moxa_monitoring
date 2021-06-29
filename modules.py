# -*- coding: utf-8 -*-

###############################################
####### Модули для программы ##################
###############################################

__metaclass__ = type

import datetime
from time import gmtime, strftime
import time
import pickle
import Tkinter as tk
import ScrolledText
import tkFont
from tkdocviewer import DocViewer
from ttk import Treeview, Frame
from Tkinter import LEFT, NO, YES, Menu, WORD, END
from tkcalendar import Calendar
import os
from collections import OrderedDict
import subprocess
from threading import Thread

from config import main_font, size_font, name_column, state_column
from config import all_values_moxa, moxa as list_moxa
from config import signalisation, time_update, time_clean_log
from config import space_X, space_Y

all_values = {key: all_values_moxa[key] for key in all_values_moxa if key in list_moxa}


def find_log():
    """ Найти лог """

    log = open('moxa.log', 'r')
    log = log.readlines()
    return log


def create_del_list():
    """ Создать лист для удаления строк из лога старше 30 дней """

    log = find_log()
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(days=30)
    del_list = []
    for i in range(len(log)):
        if log[i] != '\n':
            log_time = datetime.datetime.strptime(log[i][0:19], '%Y-%m-%d %H:%M:%S')
            if now - log_time > delta:
                del_list.append(i)
    return del_list


def delete_lines():
    """ Удалить строки из лога """

    del_list = create_del_list()
    log = find_log()
    for index in sorted(del_list, reverse=True):
        del log[index]
    with open('moxa.log', 'w+') as new:
        for item in log:
            new.write(item)


def represent_data(dif):
    """ Представление даты в удобном виде """

    if ',' in str(dif):
        result = ':'.join(str(dif).split(':')[:2])
        day_time = result.split(', ')
        day = day_time[0]
        time = day_time[1]
        hour = time.split(':')[0]
        minutes = time.split(':')[1]
        if time[0] == '0':
            state = day + ' ' + minutes + 'm'
            return state
        else:
            state = day + ' ' + hour + 'h ' + minutes + 'm'
            return state
    else:
        result = ':'.join(str(dif).split(':')[:2])
        hour = result.split(':')[0]
        minutes = result.split(':')[1]
        if hour[0] == '0':
            state = minutes + 'm'
            return state
        else:
            state = hour + 'h ' + minutes + 'm'
            return state


def load_file(name, num):
    """ Загрузить словарь из файла """

    _file = open('parameters/%s%s.pkl' % (name, num), "rb")
    result = pickle.load(_file)
    _file.close()
    return result


def dump_file(name, num, dict_new):
    """ Сохранить словарь в файл """

    _file = open("parameters/%s%s.pkl" % (name, num), "wb")
    pickle.dump(dict_new, _file)
    _file.close()


def add_comment(text_comment, num, key_channel, name):
    """ Записать комментарий в файл """

    with open('comments/comment_%s_%s.txt' % (num, key_channel), 'a+') as comment:
        comment.write('%s:\n' % name)
        for line in text_comment:
            comment.write(line)


class Comment_Widget:
    """ Виджет для создания комментариев"""

    def __init__(self, name, key):
        self.name = name
        self.key = key

    def start(self):
        """ Стартовое окно виджета """

        self.win = tk.Toplevel()
        self.win.wm_title('Добавить/Изменить комментарий для канала - %s' % self.name)
        frame_comment = Frame(self.win)
        frame_comment.pack(side=LEFT)
        frame_buttons = Frame(self.win)
        frame_buttons.pack(side=LEFT)
        self.text = ScrolledText.ScrolledText(frame_comment, height=5, width=50,
                                              font=tkFont.Font(family=main_font, size=size_font), wrap=WORD)
        self.text.pack()
        for item in all_values.keys():
            for all_dict in all_values[item][0]:
                if self.name == all_values[item][0][all_dict]:
                    if item in list_moxa:
                        with open('comments/comment_%s_%s.txt' % (item, self.key), 'a+') as comment:
                            file_log = comment.readlines()
                            self.text.delete(1.0, tk.END)
                            for element in file_log:
                                self.text.insert(tk.END, element)
        but1 = tk.Button(frame_buttons, text="Сохранить", font=tkFont.Font(family=main_font, size=size_font),
                         command=self.add_comment, activebackground='spring green', height=1, width=12)
        but2 = tk.Button(frame_buttons, text="Отмена", font=tkFont.Font(family=main_font, size=size_font),
                         command=self.win.destroy, activebackground='salmon', height=1, width=12)
        but1.pack()
        but2.pack()

    def add_comment(self):
        """ Функция сохранения и записи комментария в файл после нажатия кнопки Сохранить """

        new_message = self.text.get('1.0', END)
        if new_message != "":
            for item in all_values.keys():
                for all_dict in all_values[item][0]:
                    if self.name == all_values[item][0][all_dict]:
                        if item in list_moxa:
                            with open('comments/comment_%s_%s.txt' % (item, self.key), 'w') as comment:
                                comment.write('%s:\n' % self.name.decode('koi8-r').encode('koi8-r'))
                                comment.write(new_message)
        self.win.destroy()


def insert_text():
    """Функция для просмотра лога,
    добавляет текст в виджет"""

    win = tk.Toplevel()
    win.wm_title("Просмотр лога")
    text = ScrolledText.ScrolledText(win, height=30, width=200, font=tkFont.Font(family=main_font, size=size_font))
    text.pack(expand=True, fill='both')
    with open('moxa.log', 'r') as log:
        file_log = log.readlines()
        text.delete(1.0, tk.END)
        for element in file_log:
            text.insert(tk.END, element)
    but = tk.Button(win, text='Закрыть лог', command=win.destroy, activebackground='salmon',
                    font=tkFont.Font(family=main_font, size=size_font))
    but.pack()


def play_sound():
    """ Проигрыватель аварийной мелодии """

    os.system('/opt/csw/bin/mpg123 sound.mp3')


def show_info():
    """ Показать таблицу соответсвия """

    top = tk.Toplevel()
    top.geometry('800x1200')
    v = DocViewer(top)
    v.pack(side="top", expand=1, fill="both")
    v.display_file("info_table.pdf")
    but = tk.Button(top, text="Закрыть", command=top.destroy, activebackground='salmon',
                    font=tkFont.Font(family=main_font, size=size_font), height=2, width=10)
    but.pack()


class Tree(Treeview):
    """ Класс, формирующий таблицу """

    def __init__(self, root, frame, num, logit, all_values, list_styles_names):
        Treeview.__init__(self, root)
        self.root = root
        self.num = num
        self.frame = frame
        self.name = "MOXA-%s" % str(self.num)
        self.tree = Treeview(frame, style=list_styles_names[num])
        self.tree["columns"] = ("one", "two", "three")
        self.tree.heading("#0", text="")
        self.tree.column("#0", minwidth=0, width=5, stretch=NO)
        self.tree.heading("one", text="Port")
        self.tree.column("one", minwidth=0, width=30, stretch=NO)
        self.tree.column("two", minwidth=0, width=name_column, stretch=NO)
        self.tree.heading("three", text="State")
        self.tree.column("three", minwidth=0, width=state_column, stretch=YES)
        self.tree['height'] = 32
        self.tree.tag_configure('green', background='gray7', foreground='green2')
        self.tree.tag_configure('red', background='gray7', foreground='tomato2')
        self.tree.tag_configure('blue', background='gray7', foreground='RoyalBlue')
        self.tree.tag_configure('yellow', background='gray7', foreground='yellow')
        self.tree.tag_configure('ready', background='gray7', foreground='white')
        self.tree.tag_configure('focus', background='yellow', )
        self.tree.bind("<Motion>", self.mycallback)
        self.last_focus = None
        self.tree.pack(side=LEFT)
        self.logit = logit
        self.moxa = all_values[self.num][0]
        self.wraplength = 180
        for key in self.moxa.keys():
            self.tree.insert("", "end", values=(str(key), self.moxa[key], "<><><>"), tags=("green",))

    def mycallback(self, event):
        """ Функция, отображающая комментарий при наведении мыши на канал """

        _iid = self.tree.identify_row(event.y)
        if _iid != self.last_focus:
            if self.last_focus:
                try:
                    if self.tw:
                        self.tw.destroy()
                except:
                    pass

            if _iid:
                row = self.tree.item(_iid)
                key = row["values"][0]
                if os.path.isfile('comments/comment_%s_%s.txt' % (self.num, key)):
                    with open('comments/comment_%s_%s.txt' % (self.num, key), 'a+') as comment:
                        file_log = comment.read()
                        param = self.tree.bbox(_iid)
                        x = (param[0] + space_X) * self.num
                        y = param[1] + space_Y
                        self.tw = tk.Toplevel()
                        self.tw.wm_overrideredirect(True)
                        self.tw.wm_geometry("+%d+%d" % (x, y))
                        label = tk.Label(self.tw, text=file_log, justify='left',
                                         background="yellow2", relief='solid', borderwidth=1,
                                         wraplength=self.wraplength, font=tkFont.Font(family=main_font, size=size_font))
                        label.pack()
                self.last_focus = _iid


class AppTime(Frame):
    """ Виджет времени """

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


class ChangeStatement:
    """ Изменить состояние канала """

    def __init__(self, tree, iid, num, all_trees, logit):
        self.tree = tree
        self.iid = iid
        self.num = num
        self.all_trees = all_trees
        self.logit = logit
        self.row = self.tree.item(iid)
        self.key_tree = self.row['values'][0]
        self.all_values = all_values
        self.name = self.all_values[self.num][0][self.key_tree]
        self.add_in_table = all_values[self.num][1]


    def on_time(self):
        """ Выбрать время """

        self.top = tk.Toplevel()
        self.top.wm_title(self.name)
        lab1 = tk.Label(self.top, text='Дата и время начала работ', font=tkFont.Font(family=main_font, size=size_font))
        lab1.grid(row=0, column=0, columnspan=4, ipady=10, padx=10)
        self.cal1 = Calendar(self.top, font="Arial 14", selectmode="day", year=datetime.datetime.today().year,
                             month=datetime.datetime.today().month, day=datetime.datetime.today().day)
        self.cal1.grid(row=1, column=0, columnspan=4, rowspan=4, padx=10)
        self.time1 = AppTime(self.top)
        self.time1.grid(row=5, column=0, columnspan=4, pady=10)
        lab2 = tk.Label(self.top, text='Дата и время завершения работ',
                        font=tkFont.Font(family=main_font, size=size_font))
        lab2.grid(row=0, column=5, columnspan=4, ipady=10)
        self.cal2 = Calendar(self.top, font="Arial 14", selectmode="day", year=datetime.datetime.today().year,
                             month=datetime.datetime.today().month, day=datetime.datetime.today().day)
        self.cal2.grid(row=1, column=5, columnspan=4, rowspan=4, padx=10)
        self.time2 = AppTime(self.top)
        self.time2.grid(row=5, column=5, columnspan=4, pady=10)

        self.day1 = self.cal1.get_date()
        self.day2 = self.cal2.get_date()
        self.hour1 = self.time1.hourstr.get()
        self.hour2 = self.time2.hourstr.get()
        self.min1 = self.time1.minstr.get()
        self.min2 = self.time2.minstr.get()
        text4 = tk.Label(self.top, text='Добавьте комментарий:', font=tkFont.Font(family=main_font, size=size_font))
        text4.grid(row=6, column=0, columnspan=5, padx=10)
        self.comment_text = ScrolledText.ScrolledText(self.top, height=4, width=40,
                                                      font=tkFont.Font(family=main_font, size=size_font), wrap=WORD)
        self.comment_text.grid(row=7, column=0, columnspan=5, padx=10, pady=10)
        but1 = tk.Button(self.top, text="Выбрать",
                         command=self.select_on_time,
                         activebackground='PaleGreen1', font=tkFont.Font(family=main_font, size=size_font), height=2,
                         width=10)
        but1.grid(row=7, column=6)
        but2 = tk.Button(self.top, text="Отмена", command=self.top.destroy, activebackground='salmon',
                         font=tkFont.Font(family=main_font, size=size_font), height=2, width=10)
        but2.grid(row=7, column=7)
        self.top.resizable(height=False, width=False)

    def select_on_time(self):
        """ Отправить по времени"""

        date_order = [2, 0, 1]
        date_list1 = self.day1.split('/')
        date_list2 = self.day2.split('/')
        date_list1 = ['0' + i if len(i) == 1 else i for i in date_list1]
        date_list2 = ['0' + i if len(i) == 1 else i for i in date_list2]
        date_list1 = [date_list1[i] for i in date_order]
        date_list2 = [date_list2[i] for i in date_order]
        date_list1[0] = '20' + date_list1[0]
        date_list2[0] = '20' + date_list2[0]
        date1 = '-'.join(date_list1)
        date2 = '-'.join(date_list2)
        begin = date1 + ' ' + str(self.hour1) + ':' + str(self.min1)
        end = date2 + ' ' + str(self.hour2) + ':' + str(self.min2)
        new_value = {self.key_tree: [self.name, begin.encode('utf-8'), end.encode('utf-8')]}
        par1 = "Ремонт с".decode('koi8-r').encode('koi8-r')
        par2 = "до".decode('koi8-r').encode('koi8-r')
        for item in self.all_values.keys():
            for all_dict in self.all_values[item][0]:
                if self.name == self.all_values[item][0][all_dict]:
                    if item in list_moxa:
                        tree = self.all_trees[item]
                        remont = load_file('remont', item)
                        remont.update(new_value)
                        dump_file('remont', item, remont)
                        tree_num = self.key_tree - 1
                        row = tree.tree.get_children()[tree_num]
                        tree.tree.item(row, values=(str(self.key_tree), str(new_value[self.key_tree][0]),
                                                    "%s %s %s %s" % (
                                                        par1, new_value[self.key_tree][1], par2,
                                                        new_value[self.key_tree][2])),
                                       tags=("blue",))
                        self.logit.warning('Канал %s в MOXA%s  отправлен на ремонт на период с %s до %s' % (
                            new_value[self.key_tree][0], self.num, begin.encode('utf-8'), end.encode('utf-8')))
                        lst = [self.key_tree, str(new_value[self.key_tree][0]), "%s %s %s %s" % (
                            par1, new_value[self.key_tree][1], par2,
                            new_value[self.key_tree][2]), "blue"]
                        new_value_add = {self.key_tree: lst}
                        self.add_in_table.update(new_value_add)
                        add_comment(self.comment_text.get('1.0', END), item, self.key_tree, self.name)
        self.top.destroy()

    def on_agreement(self):
        """ Отправить в ремонт до распоряжения"""

        date_today = datetime.datetime.now()
        begin = date_today.strftime("%Y-%m-%d %H:%M")
        end = 'распоряжения'.decode('koi8-r').encode('koi8-r')
        new_value = {self.key_tree: [self.name, begin.encode('utf-8'), end]}
        par1 = "Ремонт с".decode('koi8-r').encode('koi8-r')
        par2 = "до".decode('koi8-r').encode('koi8-r')
        for item in self.all_values.keys():
            for all_dict in self.all_values[item][0]:
                if self.name == self.all_values[item][0][all_dict] and item in list_moxa:
                    tree = self.all_trees[item]
                    remont = load_file('remont', item)
                    remont.update(new_value)
                    dump_file('remont', item, remont)
                    tree_num = self.key_tree - 1
                    row = tree.tree.get_children()[tree_num]
                    tree.tree.item(row, values=(str(self.key_tree), str(new_value[self.key_tree][0]),
                                                "%s %s %s %s" % (
                                                    par1, new_value[self.key_tree][1], par2,
                                                    new_value[self.key_tree][2])),
                                   tags=("blue",))
                    self.logit.warning('Канал %s в MOXA%s  отправлен на ремонт на период с %s до %s' % (
                        new_value[self.key_tree][0], item, begin, end))
                    lst = [self.key_tree, str(new_value[self.key_tree][0]), "%s %s %s %s" % (
                        par1, new_value[self.key_tree][1], par2,
                        new_value[self.key_tree][2]), "blue"]
                    new_value_add = {self.key_tree: lst}
                    self.add_in_table.update(new_value_add)

    def return_channel(self):
        """ Вернуть канал в работу"""

        for item in self.all_values.keys():
            for all_dict in self.all_values[item][0]:
                if self.name == self.all_values[item][0][all_dict]:
                    if item in list_moxa:
                        tree = self.all_trees[item]
                        remont = load_file('remont', item)
                        for key in remont.keys():
                            if key == self.key_tree:
                                del (remont[key])
                                dump_file('remont', item, remont)
                                tree_num = self.key_tree - 1
                                row = tree.tree.get_children()[tree_num]
                                moxa = self.all_values[item][0]
                                tree.tree.item(row, values=(
                                    str(self.key_tree), str(moxa[self.key_tree]), str('updating status...')),
                                               tags=("green",))
                                self.logit.warning('Канал %s в MOXA%s возвращен в работу' % (moxa[self.key_tree], item))
                                lst = [self.key_tree, str(moxa[self.key_tree]), 'updating status...', "green"]
                                new_value_add = {self.key_tree: lst}
                                self.add_in_table.update(new_value_add)


class ControlSound:
    """ Контроль звука"""

    def __init__(self, tree, iid, num, all_tress, logit):
        self.tree = tree
        self.iid = iid
        self.num = num
        self.all_trees = all_tress
        self.logit = logit
        self.row = self.tree.item(self.iid)
        self.key_tree = self.row['values'][0]
        self.all_values = all_values_moxa
        self.name = self.all_values[self.num][0][self.key_tree]
        self.add_in_table = all_values_moxa[self.num][1]

    def mute(self):
        """ Безвучный режим"""

        new_value = {self.key_tree: 1}
        for item in self.all_values.keys():
            for all_dict in self.all_values[item][0]:
                if self.name == self.all_values[item][0][all_dict]:
                    if item in list_moxa:
                        tree = self.all_trees[item]
                        mute = load_file('mute', item)
                        mute.update(new_value)
                        dump_file('mute', item, mute)
                        tree_num = self.key_tree - 1
                        row = tree.tree.get_children()[tree_num]
                        state = 'mute' + str(self.add_in_table[self.key_tree][2])
                        tree.tree.item(row, values=(
                            str(self.add_in_table[self.key_tree][0]), str(self.add_in_table[self.key_tree][1]), state),
                                       tags=(self.add_in_table[self.key_tree][3],))
                        self.logit.warning('Канал %s в MOXA%s - mute mode on' % (
                            self.name, item))
                        lst = [self.key_tree, str(self.add_in_table[self.key_tree][1]), state,
                               self.add_in_table[self.key_tree][3]]
                        new_value_add = {self.key_tree: lst}
                        self.add_in_table.update(new_value_add)

    def loud(self):
        """ Включение звука"""

        new_value = {self.key_tree: ""}
        for item in self.all_values.keys():
            for all_dict in self.all_values[item][0]:
                if self.name == self.all_values[item][0][all_dict]:
                    if item in list_moxa:
                        tree = self.all_trees[item]
                        mute = load_file('mute', item)
                        mute.update(new_value)
                        dump_file('mute', item, mute)
                        tree_num = self.key_tree - 1
                        row = tree.tree.get_children()[tree_num]
                        tree.tree.item(row, values=(
                            str(self.add_in_table[self.key_tree][0]), str(self.add_in_table[self.key_tree][1]),
                            'updating status...'),
                                       tags=(self.add_in_table[self.key_tree][3],))
                        self.logit.warning('Канал %s в MOXA%s - mute mode off' % (
                            self.name, item))
                        lst = [self.key_tree, str(self.add_in_table[self.key_tree][1]), 'updating status...',
                               self.add_in_table[self.key_tree][3]]
                        new_value_add = {self.key_tree: lst}
                        self.add_in_table.update(new_value_add)


class ChannelLog:
    """ Показать лог по выбранному каналу """

    def __init__(self, tree, iid, num):
        self.tree = tree
        self.iid = iid
        self.num = num
        self.row = self.tree.item(iid)
        self.key_tree = self.row['values'][0]
        self.all_values = all_values
        self.name = self.all_values[self.num][0][self.key_tree]
        self.add_in_table = all_values[self.num][1]

    def read_log(self):
        """ Чтение лога"""

        win = tk.Toplevel()
        win.wm_title("Просмотр лога по каналу - %s" % self.name)
        text = ScrolledText.ScrolledText(win, height=30, width=200, font=tkFont.Font(family=main_font, size=size_font))
        text.pack(expand=True, fill='both')
        with open('moxa.log', 'r') as log:
            file_log = log.readlines()
            text.delete(1.0, tk.END)
            for line in file_log:
                if self.name in line:
                    text.insert(tk.END, line)
        but = tk.Button(win, text='Закрыть лог', command=win.destroy, activebackground='salmon',
                        font=tkFont.Font(family=main_font, size=size_font))
        but.pack()


class Popup(Menu):
    """ Выпадающие меню при нажатии ПКМ"""

    def __init__(self, master, tree, iid, num, all_trees, logit):
        Menu.__init__(self, master, tearoff=0)
        self.tree = tree
        self.iid = iid
        self.num = num
        self.all_trees = all_trees
        self.logit = logit
        self.row = self.tree.item(self.iid)
        self.key = self.row["values"][0]
        self.name = all_values[self.num][0][self.key]
        self.add_command(label="Отправить канал в ремонт до распоряжения",
                         command=lambda: ChangeStatement(self.tree, self.iid, self.num, self.all_trees,
                                                         self.logit).on_agreement(),
                         font=tkFont.Font(family=main_font, size=size_font))
        self.add_command(label="Отправить канал в ремонт по времени",
                         command=lambda: ChangeStatement(self.tree, self.iid, self.num, self.all_trees,
                                                         self.logit).on_time(),
                         font=tkFont.Font(family=main_font, size=size_font))
        self.add_command(label="Выключить звук",
                         command=lambda: ControlSound(self.tree, self.iid, self.num, self.all_trees, self.logit).mute(),
                         font=tkFont.Font(family=main_font, size=size_font))
        self.add_command(label="Показать лог по данному каналу",
                         command=lambda: ChannelLog(self.tree, self.iid, self.num).read_log(),
                         font=tkFont.Font(family=main_font, size=size_font))
        self.add_command(label="Добавить/Изменить комментарий",
                         command=lambda: Comment_Widget(self.name, self.key).start(),
                         font=tkFont.Font(family=main_font, size=size_font))
        # self.add_command(label="ТЕСТ", command =comment)
        remont = load_file('remont', num)
        mute = load_file('mute', num)
        self.bind("<FocusOut>", self.focusOut)
        if self.key in remont.keys():
            self.delete(2)
            self.delete(1)
            self.delete(0)
            self.add_command(label="Вернуть канал в работу",
                             command=lambda: ChangeStatement(tree, iid, num, all_trees, logit).return_channel(),
                             font=tkFont.Font(family=main_font, size=size_font))
        if mute[self.key] == 1:
            self.delete(2)
            self.delete(1)
            self.delete(0)
            self.add_command(label="Включить звук",
                             command=lambda: ControlSound(self.tree, self.iid, self.num, self.all_trees,
                                                          self.logit).loud(),
                             font=tkFont.Font(family=main_font, size=size_font))

        if os.path.isfile('comments/comment_%s_%s.txt' % (self.num, self.key)):
            self.add_command(label="Удалить комментарий", command=self.delete_comment,
                             font=tkFont.Font(family=main_font, size=size_font))

    def delete_comment(self):
        for item in all_values.keys():
            for all_dict in all_values[item][0]:
                if self.name == all_values[item][0][all_dict]:
                    if item in list_moxa:
                        os.system('rm comments/comment_%s_%s.txt' % (item, self.key))

    def focusOut(self, event=None):
        self.unpost()


def do_popup(event, root, num, all_trees, logit, style):
    """ Функция при нажатии ПКМ """
    tree = event.widget
    iid = tree.identify_row(event.y)
    style_str = "style%s.Treeview" % str(num)
    if iid:
        popup = Popup(root, tree, iid, num, all_trees, logit)
        row = tree.item(iid)
        color = str(row["tags"][0])
        if color == "red":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'red4')])
        elif color == "yellow":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'yellow')])
        elif color == "blue":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'blue2')])
        elif color == "ready":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'white')])
        else:
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'green2')])
        try:
            tree.selection_set(iid)
            popup.tk_popup(event.x_root, event.y_root)
        finally:
            popup.grab_release()


def do_popup2(event, num, style):
    """ Функция при нажатии ЛКМ, изменяет цвет строки по состоянию канала"""

    tree = event.widget
    iid = tree.identify_row(event.y)
    style_str = "style%s.Treeview" % str(num)
    if iid:
        row = tree.item(iid)
        color = str(row["tags"][0])
        if color == "red":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'red4')])
        elif color == "yellow":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'yellow')])
        elif color == "blue":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'blue2')])
        elif color == "ready":
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'white')])
        else:
            style.map('%s' % style_str, background=[('selected', 'gray45')], foreground=[('selected', 'green2')])


class MoxaMonitoring:
    """ Мониторинг состояния каналов """

    def __init__(self, num, logit, working_trees):
        self.working_trees = working_trees
        self.num = num
        self.tree = working_trees[num]
        self.text = "%s %s" % (self.tree.name, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        self.remember = []
        self.remont = load_file('remont', self.num)
        self.updatetime = load_file('updatetime', self.num)
        self.mute = load_file('mute', self.num)
        self.rx = load_file('rx', self.num)
        self.tx = load_file('tx', self.num)
        self.IT = load_file('IT', self.num)
        self.red = load_file('red', self.num)
        self.moxa = all_values[self.num][0]
        self.ip = all_values[self.num][2]
        self.add_in_table = all_values[self.num][1]
        self.logit = logit
        self.name = "MOXA-%s" % str(self.num)

    def update_table(self, key, state, color, add_in_table, num, updatetime):
        """ Обновить значения для каналов НЕ В РЕМОНТЕ """

        lst = [key, self.moxa[key], state, color]
        new_value = {key: lst}
        add_in_table.update(new_value)
        dump_file('updatetime', num, updatetime)

    def update_table_remont(self, key, value, state, color, add_in_table, num, updatetime):
        """ Обновить значения для каналов В РЕМОНТЕ """

        lst = [key, value, state, color]
        new_value = {key: lst}
        add_in_table.update(new_value)
        dump_file('updatetime', num, updatetime)

    def curent_rx(self, port):
        """ Отслеживание принятых пакетов """

        curentrx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % self.ip,
                                            '.1.3.6.1.2.1.2.2.1.10.%s' % port]).rstrip()

        # curentrx = 500
        return curentrx

    def cunent_tx(self, port):
        """ Отслеживание отправленных пакетов """

        curenttx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % self.ip,
                                            '.1.3.6.1.2.1.2.2.1.16.%s' % port]).rstrip()

        # curenttx = 500
        return curenttx

    def pass_values(self, add_in_table, tree):
        """ Передать значения для записи в таблицу """

        add_in_table0 = OrderedDict(sorted(add_in_table.items()))
        for key in add_in_table0.keys():
            num = key - 1
            row = tree.tree.get_children()[num]
            tree.tree.item(row,
                           values=(str(add_in_table0[key][0]), str(add_in_table0[key][1]), str(add_in_table0[key][2])),
                           tags=(add_in_table0[key][3],))

    def check_for_red(self, key):
        """ Проверить возвращение канала из неактивного состояния в активное """

        if self.red[key] == "1":
            self.logit.warning('%s - %s Канал активен' % (self.name, self.moxa[key]))
            new_value = {key: "0"}
            self.red.update(new_value)
            dump_file('red', self.num, self.red)

    def check_not_in_remont(self):
        """ Проверка состояния каналов НЕ В РЕМОНТЕ"""

        self.curentime = datetime.datetime.today()
        self.tree.tree.heading("two", text=self.text)
        for key in self.moxa.keys():

            if key not in self.remont.keys():
                port = key + 1
                curentrx = self.curent_rx(port)
                curenttx = self.cunent_tx(port)

                if curentrx != self.rx[key] or curenttx != self.tx[key]:
                    self.updatetime[key] = self.curentime
                    self.rx[key] = curentrx
                    self.tx[key] = curenttx
                    dump_file('rx', self.num, self.rx)
                    dump_file('tx', self.num, self.tx)

                    if curenttx != '0' and curentrx != '0' and self.mute[key] == "":
                        self.remember.append(key)
                        state = '<<< >>>'
                        self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)
                        self.check_for_red(key)

                    if curentrx != '0' and key not in self.remember and self.mute[key] == "":
                        state = '<<<'
                        self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)
                        self.check_for_red(key)

                    if curenttx != '0' and key not in self.remember and self.mute[key] == "":
                        state = '>>>'
                        self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)
                        self.check_for_red(key)

                    if curenttx != '0' and curentrx != '0' and self.mute[key] == 1:
                        state = 'mute' + ' <<< >>>'
                        self.remember.append(key)
                        self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)
                        self.check_for_red(key)

                    if curentrx != '0' and key not in self.remember and self.mute[key] == 1:
                        state = 'mute' + ' <<<'
                        self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)
                        self.check_for_red(key)

                    if curenttx != '0' and key not in self.remember and self.mute[key] == 1:
                        state = 'mute' + ' >>>'
                        self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)
                        self.check_for_red(key)

                self.IT[key] = self.curentime - self.updatetime[key]
                if self.IT[key] > datetime.timedelta(minutes=1) and self.IT[key] < datetime.timedelta(hours=12) and \
                        self.moxa[
                            key] != "" and self.mute[key] == "":
                    absent = represent_data(str(self.IT[key]))
                    state = str(self.updatetime[key]).split(".")[0] + ' ' + absent
                    self.update_table(key, state, 'red', self.add_in_table, self.num, self.updatetime)

                if self.IT[key] > datetime.timedelta(hours=12) and self.moxa[key] != "" and self.mute[key] == "":
                    absent = represent_data(str(self.IT[key]))
                    state = str(self.updatetime[key]).split(".")[0] + ' ' + absent
                    self.update_table(key, state, 'yellow', self.add_in_table, self.num, self.updatetime)

                if self.moxa[key] == "":
                    state = ""
                    self.update_table(key, state, 'green', self.add_in_table, self.num, self.updatetime)

                if self.IT[key] > datetime.timedelta(minutes=1) and self.IT[key] < datetime.timedelta(hours=12) and \
                        self.moxa[
                            key] != "" and self.mute[key] == 1:
                    absent = represent_data(str(self.IT[key]))
                    state = 'mute' + ' ' + str(self.updatetime[key]).split(".")[0] + ' ' + absent
                    self.update_table(key, state, 'red', self.add_in_table, self.num, self.updatetime)

                if self.IT[key] > datetime.timedelta(hours=12) and self.moxa[key] != "" and self.mute[key] == 1:
                    absent = represent_data(str(self.IT[key]))
                    state = 'mute' + ' ' + str(self.updatetime[key]).split(".")[0] + ' ' + absent
                    self.update_table(key, state, 'yellow', self.add_in_table, self.num, self.updatetime)

                if datetime.timedelta(minutes=signalisation) < self.IT[key] < datetime.timedelta(
                        minutes=signalisation + 1) and self.moxa[key] != "" and self.moxa[
                    key] != "Объединенная РЛИ для ВЕГА" and self.mute[key] != 1:
                    self.logit.warning('%s - %s пропал. Время пропадания - %s' % (
                        self.name, self.moxa[key], self.updatetime[key].replace(microsecond=0)))
                    new_value = {key: "1"}
                    self.red.update(new_value)
                    dump_file('red', self.num, self.red)
                    play_sound()

                if datetime.timedelta(minutes=signalisation) < self.IT[key] < datetime.timedelta(
                        minutes=signalisation + 1) and self.moxa[key] != "" and self.moxa[
                    key] != "Объединенная РЛИ для ВЕГА" and self.mute[key] == 1:
                    self.logit.warning('%s - %s пропал. Время пропадания - %s' % (
                        self.name, self.moxa[key], self.updatetime[key].replace(microsecond=0)))
                    new_value = {key: "1"}
                    self.red.update(new_value)
                    dump_file('red', self.num, self.red)
        self.pass_values(self.add_in_table, self.tree)

    def check_in_remont(self):
        """ Проверка состояния каналов В РЕМОНТЕ"""

        self.curentime = datetime.datetime.today()
        for key in self.remont.keys():
            port = key + 1
            rem = self.remont[key]
            name_rem = rem[0]
            par1 = "Ремонт с ".decode('koi8-r').encode('koi8-r')
            par2 = " до ".decode('koi8-r').encode('koi8-r')
            period = par1 + rem[1] + par2 + rem[2]
            lst = [key, name_rem, period, 'blue']
            new_value = {key: lst}
            self.add_in_table.update(new_value)
            curentrx = self.curent_rx(port)
            curenttx = self.cunent_tx(port)
            if curentrx != self.rx[key] or curenttx != self.tx[key]:
                self.updatetime[key] = self.curentime
                self.rx[key] = curentrx
                self.tx[key] = curenttx
                dump_file('rx', self.num, self.rx)
                dump_file('tx', self.num, self.tx)
                if curenttx != '0' and curentrx != '0' and self.mute[key] == "":
                    self.update_table_remont(key, name_rem, period, 'ready', self.add_in_table, self.num,
                                             self.updatetime)
                elif curentrx != '0' and key not in self.remember and self.mute[key] == "":
                    self.update_table_remont(key, name_rem, period, 'ready', self.add_in_table, self.num,
                                             self.updatetime)
                elif curenttx != '0' and key not in self.remember and self.mute[key] == "":
                    self.update_table_remont(key, name_rem, period, 'ready', self.add_in_table, self.num,
                                             self.updatetime)

            self.pass_values(self.add_in_table, self.tree)


def check(num, logit, working_trees):
    """ Проверка состояния в цикле """

    while True:
        try:
            check = MoxaMonitoring(num, logit, working_trees)
            check.check_in_remont()
            check.check_not_in_remont()
            time.sleep(time_update)
        except:
            pass


def clean_log():
    """ Зачистка лога в цикле"""

    while True:
        try:
            delete_lines()
            time.sleep(time_clean_log)
        except:
            pass
