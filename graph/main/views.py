from django.shortcuts import render
from .models import NodeTable
import itertools

import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt

import math


def add_value(request):
    error = 'ValueError вылезла'
    value = request.POST.get('value', '')
    index = request.POST.get('index', '')
    try:
        b = NodeTable(isValueNode=True, typeOfOperation=None, indexOfChild=index, value=value)
        b.save()
    except ValueError:
        print(error)

    return render(request, 'main/add_value.html')


def add_operation(request):
    error = 'ValueError вылезла'
    operation = request.POST.get('operation', '')
    index = request.POST.get('index', '')
    try:
        b = NodeTable(isValueNode=False, typeOfOperation=operation, indexOfChild=index, value=None)
        b.save()
    except ValueError:
        print(error)
    return render(request, 'main/add_operation.html')


def vectorConvert(*vec):
    vector_str = []
    vector = []
    indexOfBiggestStr = 0

    for i in vec:
        vector_str.append(i.replace(' ', '').split(','))

    for i in range(len(vector_str)):
        if len(vector_str[i]) > indexOfBiggestStr:
            indexOfBiggestStr = i

    for i in range(len(vector_str)):
        vector.append([0] * len(vector_str[indexOfBiggestStr]))

    for i in range(len(vector_str)):
        for j in range(len(vector_str[i])):
            vector[i][j] = int(vector_str[i][j])

    return vector


def vectorLenght(vector):
    result = [0] * len(vector)

    for i in range(len(vector)):
        for j in range(len(vector[0])):
            result[i] += math.pow(vector[i][j], 2)
        result[i] = math.fabs(math.sqrt(result[i]))

    return result


def show(request):
    v1 = "1, 8, 3"
    v2 = "2, 4, 7, 5"
    result = vectorLenght(vectorConvert(v1, v2))
    print(result)
    return render(request, "main/show.html")
