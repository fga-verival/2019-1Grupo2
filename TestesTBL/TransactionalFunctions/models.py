from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy


class TransactionalFunction(models.Model):

    name = models.CharField(verbose_name="Nome", max_length=250)

    FUNCTIONALITY_TYPE_CHOICES = (
        (1, 'EE'),
        (2, 'CE'),
        (3, 'SE')
    )

    functionality_type = models.IntegerField(verbose_name="Tipo de Funcionalidade", choices=FUNCTIONALITY_TYPE_CHOICES)

    ALR_aumount = models.IntegerField(verbose_name="Parâmetro 1 (ALR)", validators=[MinValueValidator(0)])

    DER_aumount = models.IntegerField(verbose_name="Parâmetro 2 (DER)", validators=[MinValueValidator(0)])

    counter_name = models.CharField(verbose_name="Nome do Contador", max_length=250)

    date = models.DateField(verbose_name="Data", auto_now=True)

    class Meta:
        verbose_name = "Função Transacional"
        verbose_name_plural = "Funções Transacional"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('list')

    @property
    def transactional_complexity(self):
        return None

    @property
    def function_points_aumount(self):
        return None
