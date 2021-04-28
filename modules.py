# -*- coding: utf-8 -*-
###############################################
################## Modules ####################
###############################################

def find_log():
    log = open('/sintez/sintez/moxa_monitoring/moxa.log', 'r')
    log = log.readlines()
    return log


def create_del_list():
    import datetime
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
    del_list = create_del_list()
    log = find_log()
    for index in sorted(del_list, reverse=True):
        del log[index]
    with open('/sintez/sintez/moxa_monitoring/moxa.log', 'w+') as new:
        for item in log:
            new.write(item)


def represent_data(dif):
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


# Функции для загрузки и сохранения изменения в словари
def load_file(name, num):
    import pickle
    _file = open('/sintez/sintez/moxa_monitoring/parameters/%s%s.pkl' % (name, num), "rb")
    result = pickle.load(_file)
    _file.close()
    return result


def dump_file(name, num, dict_new):
    import pickle
    _file = open("/sintez/sintez/moxa_monitoring/parameters/%s%s.pkl" % (name, num), "wb")
    pickle.dump(dict_new, _file)
    _file.close()


if __name__ == "__main__":
    delete_lines()
    represent_data()
    load_file()
    dump_file()
