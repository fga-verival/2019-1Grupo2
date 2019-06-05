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

    def get_by_transactions_type(self):
        return {
            'EE': self.sum_points_of_class(1),
            'CE': self.sum_points_of_class(2),
            'SE': self.sum_points_of_class(3)
        }

    def sum_points_of_class(self, type):

        transactions = TransactionalFunction.objects.filter(functionality_type=type)

        return sum(x.function_points_aumount for x in transactions)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['transactions_by_type'] = self.get_by_transactions_type()

        return context


class TransactionCreate(CreateView):

    model = TransactionalFunction
    form_class = TransactionalFunctionForm
    template_name = 'TransactionalFunctions/createview.html'

