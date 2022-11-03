from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from .forms import IncomeForm, ExpenseForm,DateForm
from .models import Income, Expense
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.

def index(request):
    return HttpResponse("TEST")


def new_income(request):
    if request.method == "POST":
        new_income_form = IncomeForm(request.POST)
        current_user = request.user
        if new_income_form.is_valid():
            income = new_income_form.cleaned_data["income"]
            income_amount = new_income_form.cleaned_data["income_amount"]
            newIncome = Income(user = current_user, income = income, income_amount = income_amount)
            newIncome.save()
            return HttpResponseRedirect("/user/income")
    form = IncomeForm()
    return render(request, "IncomeExpenseCalc/income_form.html", {"incomeForm":form})

def new_expense(request):
    if request.method == "POST":
        new_expense_form = ExpenseForm(request.POST)
        current_user = request.user
        if new_expense_form.is_valid():
            expense = new_expense_form.cleaned_data["expense"]
            expense_amount = new_expense_form.cleaned_data["expense_amount"]
            newExpense = Expense(user = current_user, expense = expense, expense_amount = expense_amount)
            newExpense.save()
            return HttpResponseRedirect("/user/expense")
    form = ExpenseForm()
    return render(request, "IncomeExpenseCalc/expense_form.html", {"expenseForm":form})


def user(request):
    if request.method == "POST":
        date_string = request.POST["datetime"]
        datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M')
        income_date = Income.objects.filter(income_instance_creation_date__lt=datetime_object)
        expense_data = Expense.objects.filter(expense_instance_creation_date__lt=datetime_object)
        date_form = DateForm()
        current_user = request.user
        income_objects = Income.objects.filter(user = current_user)
        expense_objects = Expense.objects.filter(user = current_user)
        on_hand=on_hand_calc(income_objects,expense_objects)
        return render(request, "IncomeExpenseCalc/user.html", {"income_objects":income_objects,"expense_objects":expense_objects,"user":current_user,"on_hand":on_hand,"date_form":date_form,"date":date_string
        ,"datetime_object":datetime_object,"income_date":income_date,"expense_data":expense_data})

    date_form = DateForm()
    current_user = request.user
    income_objects = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    on_hand=on_hand_calc(income_objects,expense_objects)
    return render(request, "IncomeExpenseCalc/user.html", {"income_objects":income_objects,"expense_objects":expense_objects,"user":current_user,"on_hand":on_hand,"date_form":date_form})

def on_hand_calc(income_objects,expense_objects):
    income_amount = 0
    income_amount = [ i.income_amount+income_amount for i in income_objects]
    expense_amount = 0
    expense_amount = [ i.expense_amount+expense_amount for i in expense_objects]
    on_hand = income_amount[0] - expense_amount[0]
    return on_hand


