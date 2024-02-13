import json
import random
from prettytable import PrettyTable
import copy

s = 'Effective Mobile'
w = 30
counter = 1 #Счётчик
prev = 0 #min число при срезе списка
nextt = 0 #max число при срезе списка


#Во время первого запуска проверяем есть ли файл, если нет то создаём
try:
    file = open('data_file.json', 'r')
except OSError:
    file = open('data_file.json', 'w')

file.close()

#Оформление заголовка программы
print('\n'.join(['*' * w, '*{:^{wid}}*'.format(s, wid=w - 2), '*' * w]))


#Функция автоматического создания словаря и его заполнения
def addToBd():
    name = ["Андрей", "Александр", "Дмитрий", "Вячеслав", "Виктор"]
    otchestvo = ["Андреевич", "Васильевич", "Анатольевич", "Николаевич", "Фёдорович"]
    surName = ["Иванов", "Петров", "Сидоров", "Стрельцов", "Пушкин"]
    firm = ["intel", "AMD", "ASUS", "MSI", "GigaByte"]
    telHome = ["+375 17 111 11 11", "+375 17 222 22 22", "+375 17 333 33 33", "+375 17 444 44 44", "+375 17 555 55 55"]
    telJob = ["+375 29 111 11 22", "+375 29 222 22 33", "+375 29 333 33 44", "+375 29 444 44 55", "+375 29 555 55 66"]

    db_dict = {"name": random.choice(name),
               "otchestvo": random.choice(otchestvo),
               "surname": random.choice(surName),
               "firm": random.choice(firm), "tel_home": random.choice(telHome),
               "tel_job": random.choice(telJob)}

    return db_dict


#Функция записи данных в файл
def recordDict(data):
    with open("data_file.json", "w", encoding="UTF-8") as file:
        our_json = json.dumps(data, indent=4)
        file.write(our_json)


#Функция в которой создаётся словарь и записываются в файл
def autoDictAdd():
    listDict = readDict() #Чтение из файла
    # listDict = []

    listDict.append(addToBd()) #Добавляем новую запись в справочник
    recordDict(listDict)        #Записываем обновленный справочник
    addDict()                   #Меню добавления данных


#Функция ручного ввода данных
def manualDictAdd():
    bd = []
    name = input("Введите Имя :")
    otchestvo = input("Введите Отчество :")
    surName = input("Введите Фамилию :")
    firm = input("Введите название фирмы :")
    telHome = input("Введите домашний телефон :")
    telJob = input("Введите рабочий телефон :")

    db_dict = {"name": name,
               "otchestvo": otchestvo,
               "surname": surName,
               "firm": firm, "tel_home": telHome,
               "tel_job": telJob}

    listDict = readDict() #Чтение из файла

    listDict.append(db_dict) #Добавление в справочник
    recordDict(listDict)      #Перезапись справочника
    addDict() #Меню добавления данных


#Функция чтения из файла
def readDict():
    with open("data_file.json", "r", encoding="UTF-8") as file:
        our_json = json.load(file)

    return (our_json)


#Меню добавления данных
def addDict():
    print("Выберите Действие:")
    print("1 - Добавить автоматически")
    print("2 - Добавить в ручную")
    print("3 - Главная страница")

    num = input("Введите число от 1 до 3 :")

    num = correct(num) #Функция проверки корретности данных

    if num == 1:
        autoDictAdd() #Автоматическое создание словаря и добавление в справочник
    if num == 2:
        manualDictAdd() #Ручное создание словаря и добавление в справочник
    if num == 3:
        start()      #Возврат в начало программы


#Функция обновления данных
def updateDict():
    listDict = readDict()
    i = 0

    print("Поиск значения:")
    search = input("Введите Имя Отчество и Фамилию ")
    [name, otchestvo, surname] = search.split(' ')
    print(name)
    print(otchestvo)
    print(surname)

    for row in listDict:
        i = + 1
        # keys = [key for key in row if row[key] == search]
        for key in row:
            if (row[key] == surname):
                print(i)
                print("Найдена строка :")
                print(row)
                print("Какое поле меняем")
                keyUpdate = input("Введите название поля")
                print("Введите новое значение поля ")
                valueUpdate = input("Введите значение поля")
                row[keyUpdate] = valueUpdate
                print(row)
                del listDict[i]
                listDict.append(row)
                recordDict(listDict)
                start()


#Функция проверки корретности данных
def correct(num):
    if num.isdigit():
        num = int(num)
        if (num >= 1 and num <= 3):
            return num
        else:
            start()
    else:
        start()


#Функция разбива массива на подмассивы
def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]





#Функция пагинации в перёд
def nextPagination(listDict, prev, nex, colPage, readRec):
    global counter

    readRec = readRec + 0

    pagList = pagination(listDict, prev, nex)
    print(prev)
    print(nex)

    table = PrettyTable()
    table.field_names = ['name', 'otchestvo', 'surname', 'firm', 'tel_home', 'tel_job']
    for row in pagList:
        table.add_row([row['name'], row['otchestvo'], row['surname'], row['firm'], row['tel_home'], row['tel_job']])

    print(table)

    print("Количество записей - ", len(listDict))
    print("Количество страниц - ", colPage)
    print("Текущее положение - ", counter, " / ", colPage)



    if (counter == colPage):
        prevMenu(listDict, prev, nex, colPage, readRec) #Меню
    else:
        menu(listDict, prev, nex, colPage, readRec)    #Меню


#Функция пагинации в назад
def prevPagination(listDict, prev, nex, colPage, readRec):
    global counter

    readRec = readRec + 0

    pagList = pagination(listDict, prev, nex)

    table = PrettyTable()
    table.field_names = ['name', 'otchestvo', 'surname', 'firm', 'tel_home', 'tel_job']
    for row in pagList:
        table.add_row([row['name'], row['otchestvo'], row['surname'], row['firm'], row['tel_home'], row['tel_job']])

    print(table)

    print("Количество записей - ", len(listDict))
    print("Количество страниц - ", colPage)
    print("Текущее положение - ", counter, " / ", colPage)

    if (counter == 1):
        nextMenu(listDict, prev, nex, colPage, readRec)
    else:
        menu(listDict, prev, nex, colPage, readRec)


def prevMenu(listDict, prev, nex, colPage, readRec):
    global counter
    print("Выберите Действие:")
    print("1 - Добавить запись")
    print("2 - Назад")
    print("3 - Главное меню")

    num = input("Введите число от 1 до 3 :")

    num = correct(num)

    if num == 1:
        addDict()
    if num == 2:
        counter = counter - 1
        nextt = nex - readRec
        prev = nex - readRec - readRec
        prevPagination(listDict, prev, nextt, colPage, readRec)
    if num == 3:
        start()


def nextMenu(listDict, prev, nex, colPage, readRec):
    global counter
    print("Выберите Действие:")
    print("1 - Добавить запись")
    print("2 - Далее")
    print("3 - Главное меню")


    num = input("Введите число от 1 до 3 :")

    num = correct(num)

    if num == 1:
        addDict()
    if num == 2:
        counter = counter + 1
        prev = nex
        nextt = prev + readRec
        nextPagination(listDict, prev, nextt, colPage, readRec)
    if num == 3:
        start()



def menu(listDict, prev, nex, colPage, readRec):
    print("readRect", readRec)
    global counter
    global nextt


    print("Выберите Действие:")
    print("1 - Далее")
    print("2 - Назад")
    print("3 - Главное меню")

    num = input("Введите число от 1 до 3 :")

    num = correct(num)

    if num == 1:
        counter = counter + 1
        prev = nex
        nextt = prev + readRec
        nextPagination(listDict, prev, nextt, colPage, readRec)
    if num == 2:
        counter = counter - 1
        nextt = prev
        prev = nextt - readRec
        print("prev ", prev)
        print("nextt ", nextt)

        prevPagination(listDict, prev, nextt, colPage, readRec)
    if num == 3:
        start()


def showTable():

    global counter
    print("Какое количество записей выводить:")
    global prev
    global nextt

    readRec = input("Введите число от 1 до 3 :")

    readRec = correct(readRec)                  #Проверка входных данных
    listDict = readDict()                       #Чтение файла

    nex = copy.copy(readRec)
    pagList = pagination(listDict, prev, nex)   #срез списка

    table = PrettyTable()          #доступное представление данных(модуль)
    table.field_names = ['name', 'otchestvo', 'surname', 'firm', 'tel_home', 'tel_job']
    for row in pagList:
        table.add_row([row['name'], row['otchestvo'], row['surname'], row['firm'], row['tel_home'], row['tel_job']])

    print(table)

    colPage = len(list(chunks(listDict, nex))) #Колиство отображаемых страниц

    listDict = readDict()
    print("Количество записей - ", len(listDict))
    print("Количество страниц - ", colPage)
    print("Текущее положение - ", counter, " / ", colPage)

    print("Выберите Действие:")

    print("1 - Далее")
    print("2 - Добавить запись")
    print("3 - Главное меню")

    num = input("Введите число от 1 до 3 :")

    num = correct(num)

    if num == 1:
        counter = counter + 1
        prev = nex
        nex = prev + readRec

        nextPagination(listDict, prev, nex, colPage, readRec)

    if num == 2:
        addDict()
    if num == 3:
        start()


#Функция среза списка
def pagination(lst, prev, nex):

    pagLst = lst[prev:nex]


    return pagLst

#Основная программа
def start():

    global counter
    global prev
    global nextt

    counter = 1
    prev = 0
    nextt = 0

    print("Выберите Действие:")
    print("1 - Вывезти записи")
    print("2 - Добавить запись")
    print("3 - Изменить запись")

    num = input("Введите число от 1 до 3 :")

    num = correct(num)

    if num == 1:
        showTable()
    if num == 2:
        addDict()
    if num == 3:
        updateDict()


start()
