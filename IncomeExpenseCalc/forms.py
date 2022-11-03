from django import forms

from .models import Income,Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ("income","income_amount")

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("expense","expense_amount")

class DateForm(forms.Form):
    datefield = forms.DateTimeField()