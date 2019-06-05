from django import forms

from TransactionalFunctions.models import TransactionalFunction


class TransactionalFunctionForm(forms.ModelForm):
    class Meta:
        model = TransactionalFunction
        fields = '__all__'
