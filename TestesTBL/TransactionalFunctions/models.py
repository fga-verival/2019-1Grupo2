from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from django.urls import reverse_lazy


class TransactionalFunction(models.Model):

    name = models.CharField(
        verbose_name="Nome",
        max_length=250,
        validators=[
            MinLengthValidator(4, message='O nome deve ter pelo menos 3 caracteres')
        ]
    )

    FUNCTIONALITY_TYPE_CHOICES = (
        (1, 'EE'),
        (2, 'CE'),
        (3, 'SE')
    )

    functionality_type = models.IntegerField(verbose_name="Tipo de Funcionalidade", choices=FUNCTIONALITY_TYPE_CHOICES)

    ALR_aumount = models.IntegerField(
        verbose_name="Parâmetro 1 (ALR)",
        validators=[
            MinValueValidator(0, message='O valor de ALR deve ser maior ou igual a 0')
        ]
    )

    DER_aumount = models.IntegerField(
        verbose_name="Parâmetro 2 (DER)",
        validators=[
            MinValueValidator(1, message='O valor de DER deve ser maior ou igual a 1')
        ]
    )

    counter_name = models.CharField(
        verbose_name="Nome do Contador",
        max_length=250,
        validators=[
            MinLengthValidator(4, message='O nome do contador deve ter pelo menos 3 caracteres')
        ]
    )

    date = models.DateField(verbose_name="Data", auto_now=True)

    MATRIX_MAP = [
        ["BAIXA", "BAIXA", "MEDIA"],
        ["BAIXA", "MEDIA", "ALTA"],
        ["MEDIA", "ALTA", "ALTA"]
    ]

    class Meta:
        verbose_name = "Função Transacional"
        verbose_name_plural = "Funções Transacional"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('list')

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def ee_functional_complexity(self):

        i = j = None

        if 0 <= self.ALR_aumount <= 1:
            i = 0
        elif self.ALR_aumount == 2:
            i = 1
        elif 3 <= self.ALR_aumount:
            i = 2

        if 1 <= self.DER_aumount <= 4:
            j = 0
        elif 5 <= self.DER_aumount <= 15:
            j = 1
        elif 16 <= self.DER_aumount:
            j = 2

        return self.MATRIX_MAP[i][j]

    def ce_functional_complexity(self):

        i = j = None

        if 0 <= self.ALR_aumount <= 1:
            i = 0
        elif 2 <= self.ALR_aumount <= 3:
            i = 1
        elif 4 <= self.ALR_aumount:
            i = 2

        if 1 <= self.DER_aumount <= 4:
            j = 0
        elif 5 <= self.DER_aumount <= 19:
            j = 1
        elif 20 <= self.DER_aumount:
            j = 2

        return self.MATRIX_MAP[i][j]

    def se_functional_complexity(self):

        i = j = None

        if 0 <= self.ALR_aumount <= 1:
            i = 0
        elif 2 <= self.ALR_aumount <= 3:
            i = 1
        elif 4 <= self.ALR_aumount:
            i = 2

        if 1 <= self.DER_aumount <= 5:
            j = 0
        elif 6 <= self.DER_aumount <= 19:
            j = 1
        elif 20 <= self.DER_aumount:
            j = 2

        return self.MATRIX_MAP[i][j]

    @property
    def transactional_complexity(self):

        function_map = {
            1: self.ee_functional_complexity,
            2: self.ce_functional_complexity,
            3: self.se_functional_complexity
        }

        return function_map[self.functionality_type]()

    @property
    def function_points_aumount(self):

        function_points = {}

        if self.functionality_type == 1:
            function_points = {
                'BAIXA': 3,
                'MEDIA': 4,
                'ALTA': 6
            }
        elif self.functionality_type == 2:
            function_points = {
                'BAIXA': 3,
                'MEDIA': 4,
                'ALTA': 6
            }
        elif self.functionality_type == 3:
            function_points = {
                'BAIXA': 4,
                'MEDIA': 5,
                'ALTA': 7
            }

        return function_points[self.transactional_complexity]
