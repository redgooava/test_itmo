from django.db import models


class NodeTable(models.Model):
    isValueNode = models.BooleanField(blank=True, null=True)  # true - узел со значением, false - узел с операцией
    typeOfOperation = models.CharField(max_length=255, blank=True, null=True)  # математическая операция
    indexOfChild = models.IntegerField(blank=True, null=True)  # индекс узла, в который отправляется результат
    value = models.CharField(max_length=255, blank=True, null=True)  # значение узла

