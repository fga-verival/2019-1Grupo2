from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from TransactionalFunctions.models import TransactionalFunction
from TransactionalFunctions.forms import TransactionalFunctionForm

# Create your views here.
class TransactionDetail(DetailView):

    model = TransactionalFunction


class TransactionList(ListView):

    model = TransactionalFunction
    template_name = 'TransactionalFunctions/listview.html'

    def get_queryset(self):
        return self.model.objects.all()


class TransactionCreate(CreateView):

    model = TransactionalFunction
    form_class = TransactionalFunctionForm
    template_name = 'TransactionalFunctions/createview.html'

