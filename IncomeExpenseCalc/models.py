from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    income_id = models.IntegerField(primary_key = True)
    income_options = [
        ("salary","salary"),
        ("Investments","Investments"),
        ("Rental","Rental"),
    ]
    income = models.CharField(choices = income_options, max_length=100)
    income_instance_creation_date = models.DateTimeField(verbose_name=("Creation date"), auto_now_add=True, null=True)
    income_amount = models.IntegerField()

    def __str__(self):
        return self.income 

    class Meta:
        ordering  = ["-income_instance_creation_date"]
        verbose_name = "Income data"

    def date_exceed(self):
        current_date = timezone.now()
        difference =  current_date - self.income_instance_creation_date
        return difference.days



class Expense(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    expense_id = models.IntegerField(primary_key = True)
    expense_options = [
        ("Housing rent","Housing rent"),
        ("Transportation","Transportation"),
        ("Food and groceries","Food and groceries"),
        ("Utility bills","Utility bills"),
    ]
    expense = models.CharField(max_length = 100, choices = expense_options)
    expense_instance_creation_date = models.DateTimeField(verbose_name=("Creation date"), auto_now_add=True, null=True)
    expense_amount = models.IntegerField()

    def __str__(self) -> str:
        return self.expense

    class Meta:
        ordering = ["-expense_instance_creation_date"]
        verbose_name = "expense data"

    def date_exceed(self):
        current_time = timezone.now()
        difference =  current_time - self.expense_instance_creation_date
        return difference.days

