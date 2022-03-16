from django.shortcuts import render
from .models import NodeTable
import itertools

import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt

import math


def add_value(request):  # добавление узла-вектора
    error = 'ValueError вылезла'
    value = request.POST.get('value', '')
    index = request.POST.get('index', '')
    try:
        b = NodeTable(isValueNode=True, typeOfOperation=None, indexOfChild=index, value=value)  # создание записи
        b.save()
    except ValueError:
        print(error)

    return render(request, 'main/add_value.html')


def add_operation(request):  # добавление узла-операции
    error = 'ValueError вылезла'
    operation = request.POST.get('operation', '')
    index = request.POST.get('index', '')
    try:
        b = NodeTable(isValueNode=False, typeOfOperation=operation, indexOfChild=index, value=None)  # создание записи
        b.save()
    except ValueError:
        print(error)
    return render(request, 'main/add_operation.html')


def edit_value(request):  # редактирование узла-вектора
    error = 'ValueError вылезла'
    idNode = request.POST.get('idNode', '')
    value = request.POST.get('value', '')
    index = request.POST.get('index', '')
    try:
        NodeTable.objects.filter(id__exact=idNode).update(value=value, indexOfChild=index)  # редактирование записи
    except ValueError:
        print(error)

    return render(request, 'main/edit_value.html')


def edit_operation(request):  # редактирование узла-операции
    error = 'ValueError вылезла'
    idNode = request.POST.get('idNode', '')
    operation = request.POST.get('operation', '')
    index = request.POST.get('index', '')
    try:
        NodeTable.objects.filter(id__exact=idNode).update(typeOfOperation=operation, indexOfChild=index)
        # редактирование записи
    except ValueError:
        print(error)

    return render(request, 'main/edit_operation.html')


def vectorConvert(*vec):  # конвертация из списка строк в список список со значениями узлов-родителей
    vector_str = []
    vector = []
    indexOfBiggestStr = 0

    for i in vec[0]:  # убираем из строк пробелы и "нарезаем" строки на элемента списка
        vector_str.append(i.replace(' ', '').split(','))

    for i in range(len(vector_str)):  # поиск самой большой строки, чтобы по ней сделать длину каждого списка из матрицы
        if len(vector_str[i]) > indexOfBiggestStr:
            indexOfBiggestStr = i

    for i in range(len(vector_str)):  # создание матрицы (пустые элементы коротких строк заполняются нулями)
        vector.append([0] * len(vector_str[indexOfBiggestStr]))

    for i in range(len(vector_str)):  # заполнение итоговой матрицы int-значениями
        for j in range(len(vector_str[i])):
            vector[i][j] = int(vector_str[i][j])

    return vector


def vectorLenght(parentsValue):  # подсчёт длины векторов
    vector = vectorConvert(parentsValue)  # конвертация в целочисленную матрицу
    result = [0] * len(vector)

    for i in range(len(vector)):
        for j in range(len(vector[0])):
            result[i] += math.pow(vector[i][j], 2)
        result[i] = math.fabs(math.sqrt(result[i]))

    return result


def vectorAddition(parentsValue):  # сложение векторов
    vector = vectorConvert(parentsValue)  # конвертация в целочисленную матрицу
    result = [0] * len(vector[0])

    for j in range(len(vector[0])):
        for i in range(len(vector)):
            result[j] += vector[i][j]

    return result


def vectorMultiplication(parentsValue):  # умножение векторов
    vector = vectorConvert(parentsValue)  # конвертация в целочисленную матрицу
    result = [1] * len(vector[0])

    for j in range(len(vector[0])):
        for i in range(len(vector)):
            result[j] *= vector[i][j]

    return result


def countingOperation():  # выполнение операции
    queryset_values_all = NodeTable.objects.all().values()  # взяли все записи из БД
    parentsValue = []  # список под значения родительских узлов
    result = []

    for i in queryset_values_all:
        if not i['isValueNode']:  # если узел является операцией
            querysetAtID = NodeTable.objects.filter(indexOfChild__exact=i['id']).values()  # queryset родительских узлов

            parentsValue.clear()

            for j in querysetAtID:
                parentsValue.append(j['value'])  # заполнение массива со значениями родительских узлов

            if i['typeOfOperation'] == 'add':
                result = str(vectorAddition(parentsValue)).replace('[', '').replace(']', '')
            elif i['typeOfOperation'] == 'multi':
                result = str(vectorMultiplication(parentsValue)).replace('[', '').replace(']', '')
            elif i['typeOfOperation'] == 'len':
                result = str(vectorLenght(parentsValue)).replace('[', '').replace(']', '')

            NodeTable.objects.filter(id__exact=i['indexOfChild']).update(value=result)
            # отправка результата в дочерний узел


def show(request):
    G = nx.DiGraph()

    countingOperation()

    queryset_values_all = NodeTable.objects.all().values()

    nodeDescription = []  # список для сбора описаний узлов

    for i in queryset_values_all:
        G.add_node(i['id'])  # отображение узла

        if i['isValueNode']:
            nodeDescription.append(str(i['id']) + ' (' + str(i['value']) + ')')
        else:
            nodeDescription.append(str(i['id']) + ' (' + str(i['typeOfOperation']) + ')')

        if not i['indexOfChild'] == 0:
            G.add_edge(i['id'], i['indexOfChild'])  # отображение направленной связи

    context = {
        'nodeDescription': nodeDescription,
    }
    nx.draw_circular(G, node_color='red', node_size=250, with_labels=True)  # настройки отображения
    G.clear()
    plt.savefig("main/static/images/graph_img.png")

    return render(request, "main/show.html", context)
