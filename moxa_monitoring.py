#-*- coding: utf-8 -*-
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
import subprocess
import os
import logging, logging.handlers
import collections
import pickle
import values
import textwrap

rem_file1 = open("/sintez/sintez/moxa_monitoring/parameters/remont1.pkl", "rb")
remont1 = pickle.load(rem_file1)
rem_file1.close()
rem_file2 = open("/sintez/sintez/moxa_monitoring/parameters/remont2.pkl", "rb")
remont2 = pickle.load(rem_file2)
rem_file2.close()
rem_file3 = open("/sintez/sintez/moxa_monitoring/parameters/remont3.pkl", "rb")
remont3 = pickle.load(rem_file3)
rem_file3.close()
rem_file4 = open("/sintez/sintez/moxa_monitoring/parameters/remont4.pkl", "rb")
remont4 = pickle.load(rem_file4)
rem_file4.close()
rem_file5 = open("/sintez/sintez/moxa_monitoring/parameters/remont5.pkl", "rb")
remont5 = pickle.load(rem_file5)
rem_file5.close()
rem_file6 = open("/sintez/sintez/moxa_monitoring/parameters/remont6.pkl", "rb")
remont6 = pickle.load(rem_file6)
rem_file6.close()


#Формирование лога

logit = logging.getLogger('logit')
handler = logging.handlers.RotatingFileHandler("/sintez/sintez/moxa_monitoring/moxa.log", mode = 'a')
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logging.Formatter.converter = time.gmtime
logit.addHandler(handler)

root = tk.Tk()
root.title("Мониторинг состояния каналов")

def insert_text():
    win = tk.Toplevel()
    win.wm_title("Просмотр лога") 
    text = ScrolledText.ScrolledText(win)
    text.pack(expand=True, fill = 'both')
    with open('/sintez/sintez/moxa_monitoring/moxa.log', 'r') as log:
        file_log = log.readlines()
        text.delete(1.0, tk.END)
        for element in file_log:
            text.insert(tk.END, element)
    but = tk.Button(win, text='Закрыть лог', command =win.destroy, activebackground='salmon')
    but.pack()


def return_channel(moxa, remont, tree, iid, num):
    row = tree.item(iid)
    key1 = row['values'][0]
    print(key1)
    rem_file = open("/sintez/sintez/moxa_monitoring/parameters/remont%s.pkl" %num, "rb")
    remont = pickle.load(rem_file)
    rem_file.close()
    for key in remont.keys():
        if key == key1:
            del(remont[key1])
            rem_file = open("/sintez/sintez/moxa_monitoring/parameters/remont%s.pkl" %num, "wb")
            pickle.dump(remont, rem_file)
            rem_file.close()
            tree_num = key1-1
            r = tree.get_children()[tree_num]
            tree.item(r, values=(str(key1), str(moxa[key1]), str('<><><>')), tags=("green",)) 
            logit.warning('Канал %s в MOXA%s возвращен в работу' %(moxa[key1], num))

menu_bar = tk.Menu(root)
menu_bar.add_command(label="Показать лог", command= lambda: insert_text())
#menu_bar.add_command(label="Вернуть канал в работу", command= lambda: return_channel())
#menu_bar.add_command(label="Exit", command= lambda: root.destroy())
root.config(menu=menu_bar)


frame = tk.Frame(root)
frame.pack()

def comment():
    top = tk.Toplevel()
    top.wm_title("Info")
    frame1 = tk.Frame(top)
    frame1.pack()
    label = tk.Label(frame1, text="Комментарий или что-нибудь еще")
    label.pack()
    but = tk.Button(frame1, text="Close", command=top.destroy)
    but.pack()

class Popup(Menu):
    def __init__(self, master, tree, moxa, remont, iid, num):
        Menu.__init__(self, master, tearoff=0)
        self.tree = tree
        self.moxa = moxa
        self.remont = remont
        self.num = num
        self.add_command(label="Отправить канал в ремонт", command=lambda: OnDoubleClick(moxa, remont, tree, iid,num))
        self.add_command(label="ТЕСТ", command =comment )
        row = tree.item(iid)
        key = row["values"][0]
        rem_file = open("/sintez/sintez/moxa_monitoring/parameters/remont%s.pkl" %num, "rb")
        remont = pickle.load(rem_file)
        self.bind("<FocusOut>", self.focusOut)
        if key in remont.keys():  
            self.delete(0)      
            self.add_command(label="Вернуть канал в работу", command = lambda: return_channel(moxa, remont, tree, iid, num))
    def focusOut(self, event=None):
        self.unpost()

def do_popup(event, root, tree, moxa, remont, num):
    iid = tree.identify_row(event.y)
    if iid:
        popup = Popup(root, tree, moxa, remont, iid, num)
        try:
            tree.selection_set(iid)
            popup.tk_popup(event.x_root, event.y_root)
        finally:
            popup.grab_release()
   

class App(Frame):
     def __init__(self, parent):
             Frame.__init__(self, parent)
             self.hourstr=tk.StringVar(self, datetime.datetime.today().hour)
             self.hour = tk.Spinbox(self,from_=0,to=23,wrap=True,textvariable=self.hourstr,width=2,state="readonly")
             self.minstr=tk.StringVar(self,datetime.datetime.today().minute)
             self.minstr.trace("w",self.trace_var)
             self.last_value = ""
             self.min = tk.Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.minstr,width=2,state="readonly")
             self.hour.grid()
             self.min.grid(row=0,column=1)
     def trace_var(self,*args):
             if self.last_value == "59" and self.minstr.get() == "0":
                     self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)
             self.last_value = self.minstr.get()


def OnDoubleClick(moxa, remont, tree, iid, num):
    row = tree.item(iid)
    key = row['values'][0]
    name = row['values'][1].encode('utf-8')
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
    but1 = ttk.Button(top, text="Выбрать", command=lambda: select(top, key, name, cal.get_date(), app1.hourstr.get(), app1.minstr.get(), cal2.get_date(), app2.hourstr.get(), app2.minstr.get() , moxa, remont, num))
    but1.pack(pady=120)
    def select(top, key, name, date1, h1, m1, date2, h2, m2, moxa, remont, num):
        begin = date1+' '+str(h1)+':'+str(m1)
        end = date2+' '+str(h2)+':'+str(m2)
        d2 = {key: [name, begin.encode('utf-8'), end.encode('utf-8')]}
        remont.update(d2)
        rem_file = open("/sintez/sintez/moxa_monitoring/parameters/remont%s.pkl" %num, "wb")
        pickle.dump(remont, rem_file)
        rem_file.close()
        tree_num = key-1
        r = tree.get_children()[tree_num]
        tree.item(r, values=(str(key), str(d2[key][0]), str(d2[key][1])), tags=("blue",)) 
        logit.warning('Канал %s в MOXA%s  отправлен на ремонт на период с %s до %s' %(d2[key][0], num, begin.encode('utf-8'), end.encode('utf-8')))
        top.destroy()



style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background="gray7",
                fieldbackground="gray7", foreground="white", font='Calibri 10', rowheight=14)
style.configure("Treeview.Heading", font='Calibri 10')

tree1 = ttk.Treeview(frame)
tree1["columns"] = ("one", "two", "three")
tree1.heading("#0", text="")
tree1.column("#0",minwidth=0,width=5, stretch=NO)
tree1.heading("one", text="Port")
tree1.column("one",minwidth=0,width=30, stretch=NO)
tree1.heading("three", text="State")
tree1.column("three",minwidth=0,width=150, stretch=YES)
tree1['height'] = 32
tree1.tag_configure('green', background='gray7', foreground='green2')
tree1.tag_configure('red', background='gray7', foreground='red2')
tree1.tag_configure('blue', background='gray7', foreground='RoyalBlue')
tree1.tag_configure('yellow', background='gray7', foreground='yellow')
tree1.tag_configure('ready', background='gray7', foreground='white')
tree1.bind("<Button-3>", lambda event: do_popup(event, root, tree1, values.moxa1, remont1, 1))
tree1.pack(side=LEFT)

tree2 = ttk.Treeview(frame)
tree2["columns"] = ("one", "two", "three")
tree2.heading("#0", text="")
tree2.column("#0",minwidth=0,width=5, stretch=NO)
tree2.heading("one", text="Port")
tree2.column("one",minwidth=0,width=30, stretch=NO)
tree2.heading("three", text="State")
tree2.column("three",minwidth=0,width=150, stretch=YES)
tree2['height'] = 32
tree2.tag_configure('green', background='gray7', foreground='green2')
tree2.tag_configure('red', background='gray7', foreground='red2')
tree2.tag_configure('blue', background='gray7', foreground='RoyalBlue')
tree2.tag_configure('yellow', background='gray7', foreground='yellow')
tree2.tag_configure('ready', background='gray7', foreground='white')
tree2.bind("<Button-3>", lambda event: do_popup(event, root, tree2, values.moxa2, remont2, 2))
tree2.pack(side=LEFT)

tree3 = ttk.Treeview(frame)
tree3["columns"] = ("one", "two", "three")
tree3.heading("#0", text="")
tree3.column("#0",minwidth=0,width=5, stretch=NO)
tree3.heading("one", text="Port")
tree3.column("one",minwidth=0,width=30, stretch=NO)
tree3.heading("three", text="State")
tree3.column("three",minwidth=0,width=150, stretch=YES)
tree3['height'] = 32
tree3.tag_configure('green', background='gray7', foreground='green2')
tree3.tag_configure('red', background='gray7', foreground='red2')
tree3.tag_configure('blue', background='gray7', foreground='RoyalBlue')
tree3.tag_configure('yellow', background='gray7', foreground='yellow')
tree3.tag_configure('ready', background='gray7', foreground='white')
tree3.bind("<Button-3>", lambda event: do_popup(event, root, tree3,values.moxa3, remont3, 3))
tree3.pack(side=LEFT)

tree4 = ttk.Treeview(frame)
tree4["columns"] = ("one", "two", "three")
tree4.heading("#0", text="")
tree4.column("#0",minwidth=0,width=5, stretch=NO)
tree4.heading("one", text="Port")
tree4.column("one",minwidth=0,width=30, stretch=NO)
tree4.heading("three", text="State")
tree4.column("three",minwidth=0,width=150, stretch=YES)
tree4['height'] = 32
tree4.tag_configure('green', background='gray7', foreground='green2')
tree4.tag_configure('red', background='gray7', foreground='red2')
tree4.tag_configure('blue', background='gray7', foreground='RoyalBlue')
tree4.tag_configure('yellow', background='gray7', foreground='yellow')
tree4.tag_configure('ready', background='gray7', foreground='white')
tree4.bind("<Button-3>", lambda event: do_popup(event, root, tree4,values.moxa4, remont4, 4))
tree4.pack(side=LEFT)

tree5 = ttk.Treeview(frame)
tree5["columns"] = ("one", "two", "three")
tree5.heading("#0", text="")
tree5.column("#0",minwidth=0,width=5, stretch=NO)
tree5.heading("one", text="Port")
tree5.column("one",minwidth=0,width=30, stretch=NO)
tree5.heading("three", text="State")
tree5.column("three",minwidth=0,width=150, stretch=YES)
tree5['height'] = 32
tree5.tag_configure('green', background='gray7', foreground='green2')
tree5.tag_configure('red', background='gray7', foreground='red2')
tree5.tag_configure('blue', background='gray7', foreground='RoyalBlue')
tree5.tag_configure('yellow', background='gray7', foreground='yellow')
tree5.tag_configure('ready', background='gray7', foreground='white')
tree5.bind("<Button-3>", lambda event: do_popup(event, root, tree5,values.moxa5, remont5, 5))
tree5.pack(side=LEFT)

tree6 = ttk.Treeview(frame)
tree6["columns"] = ("one", "two", "three")
tree6.heading("#0", text="")
tree6.column("#0",minwidth=0,width=5, stretch=NO)
tree6.heading("one", text="Port")
tree6.column("one",minwidth=0,width=30, stretch=NO)
tree6.heading("three", text="State")
tree6.column("three",minwidth=0,width=150, stretch=YES)
tree6['height'] = 32
tree6.tag_configure('green', background='gray7', foreground='green2')
tree6.tag_configure('red', background='gray7', foreground='red2')
tree6.tag_configure('blue', background='gray7', foreground='RoyalBlue')
tree6.tag_configure('yellow', background='gray7', foreground='yellow')
tree6.tag_configure('ready', background='gray7', foreground='white')
tree6.bind("<Button-3>", lambda event: do_popup(event, root, tree6,remont6, tree6, 6))
tree6.pack(side=LEFT)

def insert_to_table(moxa, tree):
    for key in moxa.keys():
        tree.insert("", "end", values=(str(key), moxa[key], "<><><>"), tags = ("green", ))

insert_to_table(values.moxa1, tree1)
insert_to_table(values.moxa2, tree2)
insert_to_table(values.moxa3, tree3)
insert_to_table(values.moxa4, tree4)
insert_to_table(values.moxa5, tree5)
insert_to_table(values.moxa6, tree6)

def wrap(string, lenght=15):
	return '\n'.join(textwrap.wrap(string, lenght))

def moxa_func(ip, tree, name, moxa, rx, tx,  updatetime, IT, add_in_table, rem_num):
    curenttime = datetime.datetime.today()
    text = "%s %s" %(name, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    tree.heading("two", text=text)
    tree.column("two",minwidth=0,width=210, stretch=NO)
    remember = []
    rem_file = open("/sintez/sintez/moxa_monitoring/parameters/remont%s.pkl" %rem_num, "rb")
    remont = pickle.load(rem_file)
    rem_file.close()
    upd_file = open("/sintez/sintez/moxa_monitoring/parameters/updatetime%s.pkl" %rem_num, "rb")
    updatetime = pickle.load(upd_file)
    upd_file.close()
    rx_file = open("/sintez/sintez/moxa_monitoring/parameters/rx%s.pkl" %rem_num, "rb")
    rx = pickle.load(rx_file)
    rx_file.close()
    tx_file = open("/sintez/sintez/moxa_monitoring/parameters/tx%s.pkl" %rem_num, "rb")
    tx = pickle.load(tx_file)
    tx_file.close()
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
                rx_file = open("/sintez/sintez/moxa_monitoring/parameters/rx%s.pkl" %rem_num, "wb")
                pickle.dump(rx, rx_file)
                rx_file.close()
                tx_file = open("/sintez/sintez/moxa_monitoring/parameters/tx%s.pkl" %rem_num, "wb")
                pickle.dump(tx, tx_file)
                tx_file.close()
                if curenttx != '0' and curentrx != '0':
                    state = '<<< >>>'
                    remember.append(key)
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    upd_file = open("/sintez/sintez/moxa_monitoring/parameters/updatetime%s.pkl" %rem_num, "wb")
                    pickle.dump(updatetime, upd_file)
                    upd_file.close()
                if curentrx != '0' and key not in remember:
                    state = '<<<'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    upd_file = open("/sintez/sintez/moxa_monitoring/parameters/updatetime%s.pkl" %rem_num, "wb")
                    pickle.dump(updatetime, upd_file)
                    upd_file.close()
                if curenttx != '0' and key not in remember:
                    state = '>>>'
                    lst = [key, moxa[key], state, 'green']
                    d = {key: lst}
                    add_in_table.update(d)
                    upd_file = open("/sintez/sintez/moxa_monitoring/parameters/updatetime%s.pkl" %rem_num, "wb")
                    pickle.dump(updatetime, upd_file)
                    upd_file.close()
	    IT[key] = curenttime - updatetime[key]      
            if IT[key] > datetime.timedelta(minutes=1) and IT[key] < datetime.timedelta(hours=12) and  moxa[key] !="":
                upd_file = open("/sintez/sintez/moxa_monitoring/parameters/updatetime%s.pkl" %rem_num, "wb")
                pickle.dump(updatetime, upd_file)
                upd_file.close()
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
            if datetime.timedelta(minutes=2) < IT[key] < datetime.timedelta(minutes =3) and moxa[key] != "" and moxa[key] !="Объединенная РЛИ для ВЕГА" :
#                    win = tk.Toplevel()
#                    win.wm_title("Внимание")
#                    l = tk.Label(win, text = "%s - %s пропал %s" %(name, moxa[key], updatetime[key].replace(microsecond=0)))
#                    l.grid(row=0, column=0)
#                    b = ttk.Button(win, text="Хорошо", command=win.destroy)
#                    b.grid(row=1, column=0)
                    logit.warning('%s - %s пропал. Время пропадания - %s' %(name, moxa[key], updatetime[key].replace(microsecond=0)))
                    os.system('/opt/csw/bin/mpg123 /sintez/sintez/moxa_monitoring/sound.mp3')
            if datetime.timedelta(minutes=30) < IT[key] < datetime.timedelta(minutes =31) and  moxa[key] =="Объединенная РЛИ для ВЕГА" :
#                    win = tk.Toplevel()
#                    win.wm_title("Внимание")
#                    l = tk.Label(win, text = "%s - %s пропал %s" %(name, moxa[key], updatetime[key].replace(microsecond=0)))
#                    l.grid(row=0, column=0)
#                    b = ttk.Button(win, text="Хорошо", command=win.destroy)
#                    b.grid(row=1, column=0)
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
                rx_file = open("/sintez/sintez/moxa_monitoring/parameters/rx%s.pkl" %rem_num, "wb")
                pickle.dump(rx, rx_file)
                rx_file.close()
                tx_file = open("/sintez/sintez/moxa_monitoring/parameters/tx%s.pkl" %rem_num, "wb")
                pickle.dump(tx, tx_file)
                tx_file.close()
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

     

a= 50

def clean_func1():
     while True:
             try:
                     moxa_func('moxa1', tree1, "MOXA-1", values.moxa1, values.rx1, values.tx1, values.updatetime1, values.IT1, values.add_in_table1,  1)
                     time.sleep(a)
             except:
                     pass

def clean_func2():
     while True:
             try:
                     moxa_func('moxa2', tree2, "MOXA-2", values.moxa2, values.rx2, values.tx2, values.updatetime2, values.IT2, values.add_in_table2,  2)
                     time.sleep(a)
             except:
                     pass

def clean_func3():
     while True:
             try:
                     moxa_func('moxa3', tree3, "MOXA-3", values.moxa3, values.rx3, values.tx3, values.updatetime3, values.IT3, values.add_in_table3,  3)
                     time.sleep(a)
             except:
                     pass

def clean_func4():
     while True:
             try:
                     moxa_func('moxa4', tree4, "MOXA-4", values.moxa4, values.rx4, values.tx4,  values.updatetime4,values.IT4, values.add_in_table4,  4)
                     time.sleep(a)
             except:
                     pass

def clean_func5():
     while True:
             try:
                     moxa_func('moxa1', tree5, "MOXA-5", values.moxa5, values.rx5, values.tx5, values.updatetime5,values.IT5, values.add_in_table5,  5)
                     time.sleep(a)
             except:
                     pass

def clean_func6():
     while True:
             try:
                     moxa_func('moxa2', tree6, "MOXA-6", values.moxa6, values.rx6, values.tx6, values.updatetime6, values.IT6, values.add_in_table6,  6)
                     time.sleep(a)
             except:
                     pass



x1 = Thread(target=clean_func1)
x1.start()
x2 = Thread(target=clean_func2)
x2.start()
x3 = Thread(target=clean_func3)
x3.start()
x4 = Thread(target=clean_func4)
x4.start()
x5 = Thread(target=clean_func5)
x5.start()
x6 = Thread(target=clean_func6)
x6.start()
root.resizable()
root.mainloop()
