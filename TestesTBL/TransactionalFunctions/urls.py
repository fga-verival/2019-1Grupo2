from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionList.as_view(), name='list'),
    path('create', views.TransactionCreate.as_view(), name='create'),
    path('findValues/<int:type>/<int:der>/<int:alr>', views.FindValuesView.as_view(), name='findValues')
]
