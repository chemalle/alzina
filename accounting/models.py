from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import models
from django_pandas.managers import DataFrameManager
from django.forms import ModelForm

# Create your models here.


class Accounting(models.Model):
    company = models.CharField(max_length=200)
    history = models.CharField(max_length=200)
    date = models.DateField()
    debit = models.CharField(max_length=100)
    credit = models.CharField(max_length=100)
    amount = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)
    conta_devedora = models.CharField(max_length=200)
    conta_credora = models.CharField(max_length=200)
    objects = models.Manager()
    pdobjects = DataFrameManager()  # Pandas-Enabled Manager



    def __str__(self):
        return self.history


class Input(models.Model):
    email = models.EmailField(blank=True)

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = '__all__'
