#-*- coding: utf-8 -*-

###############################################
####### Скрипт для мониторинга каналов ########
###############################################

import Tkinter
import ttk
from ttk import *
import Tkinter as tk
from Tkinter import *
import ScrolledText
import datetime
import time
from time import gmtime, strftime
from tkcalendar import Calendar
from threading import Thread
import multiprocessing
import subprocess
import os
import logging, logging.handlers
import collections
import pickle
import textwrap
import config

#Определяем количество MOXA для мониторинга из конфига
list_moxa = config.moxa

#Функции для загрузки и сохранения изменения в словари
def load_file(name, num):
    _file = open('/sintez/sintez/moxa_monitoring/parameters/%s%s.pkl' % (name, num), "rb")
    result = pickle.load(_file)
    _file.close()
    return result

def dump_file(name, num, dict_new):
    _file = open("/sintez/sintez/moxa_monitoring/parameters/%s%s.pkl" % (name, num), "wb")
    pickle.dump(dict_new, _file)
    _file.close()


#Формирование лога
logit = logging.getLogger('logit')
handler = logging.handlers.RotatingFileHandler("%smoxa.log% config.folder_path", mode = 'a')
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logging.Formatter.converter = time.gmtime
logit.addHandler(handler)

#Создание основного окна
root = tk.Tk()
root.title("Мониторинг состояния каналов")

#Функция для просмотра лога
def insert_text():
    win = tk.Toplevel()
    win.wm_title("Просмотр лога") 
    text = ScrolledText.ScrolledText(win)
    text.pack(expand=True, fill = 'both')
    with open('%smoxa.log% config.folder_path', 'r') as log:
        file_log = log.readlines()
        text.delete(1.0, tk.END)
        for element in file_log:
            text.insert(tk.END, element)
    but = tk.Button(win, text='Закрыть лог', command =win.destroy, activebackground='salmon')
    but.pack()


#Вернуть канал в работу
class Popup(Menu):
    def __init__(self, master, tree, iid, num):
        Menu.__init__(self, master, tearoff=0)
        self.tree = tree
        self.num = num
        self.add_command(label="Отправить канал в ремонт", command=lambda: OnDoubleClick(tree, iid,num))
        self.add_command(label="ТЕСТ", command =comment)
        row = tree.item(iid)
        key = row["values"][0]
        rem_file = open("/sintez/sintez/moxa_monitoring/parameters/remont%s.pkl" %num, "rb")
        remont = pickle.load(rem_file)
        self.bind("<FocusOut>", self.focusOut)
        if key in remont.keys():
            self.delete(0)
            self.add_command(label="Вернуть канал в работу", command = lambda: return_channel(tree,iid, num))
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



#Функция для возвращения канала в работу
def return_channel(tree, iid, num):
     row = tree.item(iid)
     key_tree = row['values'][0]
     all_values = config.all_values_moxa
     name = all_values[num][0][key_tree]
     for x in all_values.keys():
             for all_dict in all_values[x][0]:
                     if name == all_values[x][0][all_dict]:
                             if x in list_moxa:
                                     tree = all_trees[x]
                                     remont = load_file('remont', x)
                                     for key in remont.keys():
                                             if key == key_tree:
                                                     del(remont[key])
                                                     dump_file('remont', x, remont)
                                                     tree_num = key_tree-1
                                                     r = tree.get_children()[tree_num]
					             moxa = all_values[x][0]
                                                     tree.item(r, values=(str(key_tree), str(moxa[key_tree]), str('<><><>')), tags=("green",))
						     logit.warning('Канал %s в MOXA%s возвращен в работу' % (moxa[key_tree], x))



def comment():
    top = tk.Toplevel()
    top.wm_title("Info")
    frame1 = tk.Frame(top)
    frame1.pack()
    label = tk.Label(frame1, text="Комментарий или что-нибудь еще")
    label.pack()
    but = tk.Button(frame1, text="Close", command=top.destroy)
    but.pack()


#Класс времени
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.hourstr = tk.StringVar(self, datetime.datetime.today().hour)
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hourstr, width=2, state="readonly")
        self.minstr = tk.StringVar(self, datetime.datetime.today().minute)
        self.minstr.trace("w", self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minstr, width=2, state="readonly")
        self.hour.grid()
        self.min.grid(row=0, column=1)

    def trace_var(self, *args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get()) + 1 if self.hourstr.get() != "23" else 0)
        self.last_value = self.minstr.get()


#Функция добавления канала в ремонт
def OnDoubleClick(tree, iid, num):
    row = tree.item(iid)
    key_tree = row['values'][0]
    all_values = config.all_values_moxa
    name = all_values[num][0][key_tree]
    top = tk.Toplevel()
    top.wm_title(name)
    frame1 = tk.Frame(top)
    frame1.pack(side=LEFT)
    frame2 = tk.Frame(top)
    frame2.pack(side=LEFT)
    lab1 = tk.Label(frame1, text='Дата и время начала работ')
    lab1.pack()
    cal = Calendar(frame1, font="Arial 14", selectmode="day", year=datetime.datetime.today().year,
                   month=datetime.datetime.today().month, day=datetime.datetime.today().day)
    cal.pack()
    app1 = App(frame1)
    app1.pack()
    lab2 = tk.Label(frame2, text='Дата и время завершения работ')
    lab2.pack()
    cal2 = Calendar(frame2, font="Arial 14", selectmode="day", year=datetime.datetime.today().year,
                    month=datetime.datetime.today().month, day=datetime.datetime.today().day)
    cal2.pack()
    app2 = App(frame2)
    app2.pack()
    but1 = ttk.Button(top, text="Выбрать",
                      command=lambda: select(top, key_tree, name, cal.get_date(), app1.hourstr.get(), app1.minstr.get(),
                                             cal2.get_date(), app2.hourstr.get(), app2.minstr.get(), num))
    but1.pack(pady=120)

    def select(top, key_tree, name, date1, h1, m1, date2, h2, m2, num):
        begin = date1 + ' ' + str(h1) + ':' + str(m1)
        end = date2 + ' ' + str(h2) + ':' + str(m2)
        d2 = {key_tree: [name, begin.encode('utf-8'), end.encode('utf-8')]}
	all_values = config.all_values_moxa
	for x in all_values.keys():
             for all_dict in all_values[x][0]:
                     if name == all_values[x][0][all_dict]:
                             if x in list_moxa:
                                     tree = all_trees[x]
        			     remont_new = config.all_values_moxa[x][5]
        			     remont_new.update(d2)
        			     dump_file('remont', x, remont_new)
        			     tree_num = key_tree - 1
        			     r = tree.get_children()[tree_num]
        			     tree.item(r, values=(str(key_tree), str(d2[key_tree][0]), str(d2[key_tree][1])), tags=("blue",))
                                     logit.warning('Канал %s в MOXA%s  отправлен на ремонт на период с %s до %s' % (d2[key_tree][0], num, begin.encode('utf-8'), end.encode('utf-8')))
        top.destroy()



#Формирование меню
menu_bar = tk.Menu(root)
menu_bar.add_command(label="Показать лог", command= lambda: insert_text())
menu_bar.add_command(label="Exit", command= lambda: root.destroy())
root.config(menu=menu_bar)


#Формирование раздела, в который будут помещаться таблицы
frame = tk.Frame(root)
frame.pack()

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background="gray7",
                fieldbackground="gray7", foreground="white", font='Calibri 10', rowheight=14)
style.configure("Treeview.Heading", font='Calibri 10')

#Функция для формирования таблицы со значениями
def make_tree(num):
     tree = ttk.Treeview(frame)
     tree["columns"] = ("one", "two", "three")
     tree.heading("#0", text="")
     tree.column("#0",minwidth=0,width=5, stretch=NO)
     tree.heading("one", text="Port")
     tree.column("one",minwidth=0,width=30, stretch=NO)
     tree.heading("three", text="State")
     tree.column("three",minwidth=0,width=150, stretch=YES)
     tree['height'] = 32
     tree.tag_configure('green', background='gray7', foreground='green2')
     tree.tag_configure('red', background='gray7', foreground='red2')
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
    insert_to_table(config.all_values_moxa[1][0], tree1)
    insert_to_table(config.all_values_moxa[2][0], tree2)
    insert_to_table(config.all_values_moxa[3][0], tree3)
    insert_to_table(config.all_values_moxa[4][0], tree4)

if len(list_moxa) == 6:
    insert_to_table(config.all_values_moxa[1][0], tree1)
    insert_to_table(config.all_values_moxa[2][0], tree2)
    insert_to_table(config.all_values_moxa[3][0], tree3)
    insert_to_table(config.all_values_moxa[4][0], tree4)
    insert_to_table(config.all_values_moxa[5][0], tree5)
    insert_to_table(config.all_values_moxa[6][0], tree6)

def moxa_func(tree, num):
    curenttime = datetime.datetime.today()
    name = "MOXA-%s" %num
    text = "%s %s" %(name, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    tree.heading("two", text=text)
    tree.column("two",minwidth=0,width=210, stretch=NO)
    remember = []
    remont = load_file('remont', num)
    updatetime = load_file('updatetime', num)
    rx = load_file('rx', num)
    tx = load_file('tx', num)
    IT = load_file('IT', num)
    moxa = config.all_values_moxa[num][0]
    ip = config.all_values_moxa[num][7]
    add_in_table = config.all_values_moxa[num][6]
    for key in remont.keys():
        rem = remont[key]
        name_rem = rem[0]
        period = rem[1]+' до '+rem[2]
        lst = [key, name_rem, period, 'blue' ]
        d = {key: lst}
        add_in_table.update(d)
    for key in moxa.keys():
        if key not in remont.keys():
            port = key+1
            curentrx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip, '.1.3.6.1.2.1.2.2.1.10.%s' % port]).rstrip()
            curenttx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip, '.1.3.6.1.2.1.2.2.1.16.%s' % port]).rstrip()
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                if curenttx != '0' and curentrx != '0':
                    state = '<<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curentrx != '0' and key not in remember:
                    state = '<<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
                if curenttx != '0' and key not in remember:
                    state = '>>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    dump_file('updatetime', num, updatetime)
	    IT[key] = curenttime - updatetime[key]
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and  moxa[key] !="":
                dump_file('updatetime', num, updatetime)
                state = str(updatetime[key]).split(".")[0]
                lst = [key, moxa[key], state, 'red']
                d = {key: lst}
                add_in_table.update(d)
            if IT[key] > datetime.timedelta(hours=12) and  moxa[key] !="":
                state = str(updatetime[key]).split(".")[0]
                lst = [key, moxa[key], state, 'yellow']
                d = {key: lst}
                add_in_table.update(d)
            if moxa[key] == "":
                lst = [key, "", "", 'green']
                d = {key: lst}
                add_in_table.update(d)
                #Условие для всех каналов, кроме РЛИ_для_ВЕГА (при пропадании более чем на 2 мин загорается красным)
            if datetime.timedelta(minutes=2) < IT[key] < datetime.timedelta(minutes =3) and moxa[key] != "" and moxa[key] !="Объединенная РЛИ для ВЕГА" :
                    logit.warning('%s - %s пропал. Время пропадания - %s' %(name, moxa[key], updatetime[key].replace(microsecond=0)))
                    os.system('/opt/csw/bin/mpg123 /sintez/sintez/moxa_monitoring/sound.mp3')
                #Условие для РЛИ_ВЕГА (при пропадании более чем на 30 мин загорается красным)
            if datetime.timedelta(minutes=30) < IT[key] < datetime.timedelta(minutes =31) and  moxa[key] =="Объединенная РЛИ для ВЕГА" :
                    logit.warning('%s - %s пропал. Время пропадания - %s' %(name, moxa[key], updatetime[key].replace(microsecond=0)))
                    os.system('/opt/csw/bin/mpg123 /sintez/sintez/moxa_monitoring/sound.mp3')
    for key in moxa.keys():
        if key in remont.keys():
            port = key+1
            curentrx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip, '.1.3.6.1.2.1.2.2.1.10.%s' % port]).rstrip()
            curenttx = subprocess.check_output(['snmpget', '-c', 'public', '-v', '2c', '-O', 'qv', '%s' % ip, '.1.3.6.1.2.1.2.2.1.16.%s' % port]).rstrip()
            if curentrx != rx[key] or curenttx != tx[key]:
                updatetime[key] = curenttime
                rx[key] = curentrx
                tx[key] = curenttx
                dump_file('rx', num, rx)
                dump_file('tx', num, tx)
                if curenttx != '0' and curentrx != '0':
                    rem = remont[key]
                    name_rem = rem[0]
                    period = rem[1]+' до '+rem[2]
                    lst = [key, name_rem, period, 'ready' ]
                    d = {key: lst}
                    add_in_table.update(d)
                if curentrx != '0' and key not in remember:
                    rem = remont[key]
                    name_rem = rem[0]
                    period = rem[1]+' до '+rem[2]
                    lst = [key, name_rem, period, 'ready' ]
                    d = {key: lst}
                    add_in_table.update(d)
                if curenttx != '0' and key not in remember:
                    rem = remont[key]
                    name_rem = rem[0]
                    period = rem[1]+' до '+rem[2]
                    lst = [key, name_rem, period, 'ready' ]
                    d = {key: lst}
                    add_in_table.update(d)
    add_in_table = collections.OrderedDict(sorted(add_in_table.items()))
    for key in add_in_table.keys():
        num = key -1
        r = tree.get_children()[num]
        tree.item(r, values=(str(add_in_table[key][0]), str(add_in_table[key][1]), str(add_in_table[key][2])), tags=(add_in_table[key][3],))

#Значение паузы
a= 50

#Функция запуска бесконечного цикла мониторинга
def start_function(tree, num):
    while True:
        try:
            moxa_func(tree, num)
            time.sleep(a)
        except:
            pass



#Запуск параллельных потоков
if len(list_moxa) == 4:
    x1 = Thread(target=start_function, args=(tree1, 1,))
    x1.start()

    x2 = Thread(target=start_function, args=(tree2, 2,))
    x2.start()

    x3 = Thread(target=start_function, args=(tree3, 3,))
    x3.start()

    x4 = Thread(target=start_function, args=(tree4, 4,))
    x4.start()


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


root.resizable()
root.mainloop()

