from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionList.as_view(), name='list'),
    path('create', views.TransactionCreate.as_view(), name='create'),
]
