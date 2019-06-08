import simplejson
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, View

from TransactionalFunctions.models import TransactionalFunction
from TransactionalFunctions.forms import TransactionalFunctionForm


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
        context['base_request_url'] = reverse('list');

        return context


class TransactionCreate(CreateView):

    model = TransactionalFunction
    form_class = TransactionalFunctionForm
    template_name = 'TransactionalFunctions/createview.html'


class FindValuesView(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        alr = self.kwargs['alr']
        der = self.kwargs['der']
        type = self.kwargs['type']

        mock_transaction = TransactionalFunction(
            name="mock",
            counter_name="mock",
            functionality_type=type,
            ALR_aumount=alr,
            DER_aumount=der,
            date='2000-01-01'
        )

        data = {
            'functions_points': mock_transaction.function_points_aumount,
            'complexity': mock_transaction.transactional_complexity
        }

        data = simplejson.dumps(data)

        return HttpResponse(data, content_type='application/json')
