from django.urls import path
from . import views

urlpatterns = [
    path('show', views.show, name='show'),
    path('add_value', views.add_value, name='add_value'),
    path('add_operation', views.add_operation, name='add_operation'),
]