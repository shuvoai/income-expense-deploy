from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from .forms import IncomeForm, ExpenseForm,DateForm
from .models import Income, Expense
from django.contrib.auth.models import User
from datetime import datetime,timezone
from django.db.models import Sum
from .service import *

# Create your views here.

def index(request):
    return HttpResponse("TEST")


def user(request):
    current_user = request.user
    income_objects = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    on_hand=on_hand_calc(income_objects,expense_objects)

    income_sum = Income.objects.filter(user = current_user).aggregate(Sum('income_amount'))["income_amount__sum"]
    expense_sum = Expense.objects.filter(user = current_user).aggregate(Sum('expense_amount'))["expense_amount__sum"]
    income_expense_sum_list = [income_sum,expense_sum]
    
  

    is_income = Income.objects.values_list('income', flat=True)
    is_expense = Expense.objects.values_list('expense', flat=True)
    income_this_month_sum = Income.objects.filter(user= request.user).filter(income_instance_creation_date__month = datetime.now().month).aggregate(Sum('income_amount'))["income_amount__sum"]
    expense_this_month_sum = Expense.objects.filter(user= request.user).filter(expense_instance_creation_date__month = datetime.now().month).aggregate(Sum('expense_amount'))["expense_amount__sum"]
    
    #
    income_instances_list = Income.objects.filter(user = request.user).values_list('income','income_instance_creation_date','income_amount')
    expense_instances_list = Expense.objects.filter(user = request.user).values_list('expense','expense_instance_creation_date','expense_amount')

    income_expense = list(income_instances_list) + list(expense_instances_list)
    
    sorted_income_expense = sorted(income_expense, key= lambda x : x[1],reverse=True)
    
    date_exceed = [(datetime.now(timezone.utc)- i[1]).days for i in sorted_income_expense]


    #
    income_log_date_ago_tuple = list(zip(sorted_income_expense,date_exceed))[:10]

    return render(request, "IncomeExpenseCalc/user.html", {"income_amount":income_this_month_sum,"expense_amount":expense_this_month_sum,"income_log_date_ago_tuple":income_log_date_ago_tuple,"is_income":is_income,"is_expense":is_expense,"on_hand":on_hand,"income_expense_sum_list":income_expense_sum_list,})


def income(request):
    if request.method == "POST":
        #New Income
        new_income_form = IncomeForm(request.POST)
        current_user = request.user
        if new_income_form.is_valid():
            income = new_income_form.cleaned_data["income"]
            income_amount = new_income_form.cleaned_data["income_amount"]
            newIncome = Income(user = current_user, income = income, income_amount = income_amount)
            newIncome.save()
            return HttpResponseRedirect("/user/income/")
    income_instances_list = Income.objects.filter(user = request.user).values_list('income','income_instance_creation_date','income_amount')
    date_exceed = [(datetime.now(timezone.utc)- i[1]).days for i in income_instances_list]
    income_log_date_ago_tuple = list(zip(income_instances_list,date_exceed))[:5]


    income_amount_sum_list = Income.objects.filter(user = request.user).values("income").annotate(sum_products = Sum("income_amount")).order_by('income')

    incomeform = IncomeForm()
    

    current_user = request.user
    income_objects = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    on_hand=on_hand_calc(income_objects,expense_objects)
    return render(request, "IncomeExpenseCalc/income.html",{"incomeform":incomeform,"income_objects":income_objects,"income_log_date_ago_tuple":income_log_date_ago_tuple,"income_amount_sum_list":income_amount_sum_list,"on_hand":on_hand})

def expense(request):
    expense_instances_list = Expense.objects.filter(user = request.user).values_list('expense','expense_instance_creation_date','expense_amount')
    date_exceed = [(datetime.now(timezone.utc)- i[1]).days for i in expense_instances_list]
    expense_log_date_ago_tuple = list(zip(expense_instances_list,date_exceed))[:4]  
    
    expense_amount_sum_list = Expense.objects.filter(user = request.user).values("expense").annotate(sum_products = Sum("expense_amount")).order_by('expense')

    if request.method == "POST":
        new_expense_form = ExpenseForm(request.POST)
        current_user = request.user
        if new_expense_form.is_valid():
            expense = new_expense_form.cleaned_data["expense"]
            expense_amount = new_expense_form.cleaned_data["expense_amount"]
            newExpense = Expense(user = current_user, expense = expense, expense_amount = expense_amount)
            newExpense.save()
            return HttpResponseRedirect("/user/expense/")
    
    # Use Annotate
    expenseform = ExpenseForm()
    current_user = request.user
    income_objects = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    on_hand=on_hand_calc(income_objects,expense_objects)
    return render(request, "IncomeExpenseCalc/expense.html",{"expenseform":expenseform,"expense_objects":expense_objects,"expense_log_date_ago_tuple":expense_log_date_ago_tuple,"expense_amount_sum_list":expense_amount_sum_list,"on_hand":on_hand})


def new_income(request):
    if request.method == "POST":
        new_income_form = IncomeForm(request.POST)
        current_user = request.user
        if new_income_form.is_valid():
            income = new_income_form.cleaned_data["income"]
            income_amount = new_income_form.cleaned_data["income_amount"]
            newIncome = Income(user = current_user, income = income, income_amount = income_amount)
            newIncome.save()
            return HttpResponseRedirect("/user/")
    
    data = {
        'income_amount': 'Insert your income amount',
        }
    income_objects = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    form = IncomeForm(data)
    
    return render(request, "IncomeExpenseCalc/user_test.html", {"incomeForm":form,"income_objects":income_objects,"expense_objects":expense_objects})
    
    

def new_expense(request):
    if request.method == "POST":
        new_expense_form = ExpenseForm(request.POST)
        current_user = request.user
        if new_expense_form.is_valid():
            expense = new_expense_form.cleaned_data["expense"]
            expense_amount = new_expense_form.cleaned_data["expense_amount"]
            newExpense = Expense(user = current_user, expense = expense, expense_amount = expense_amount)
            newExpense.save()
            return HttpResponseRedirect("/user/")
    income_objects = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    form = ExpenseForm()
    return render(request, "IncomeExpenseCalc/user_test.html", {"expenseForm":form,"income_objects":income_objects,"expense_objects":expense_objects})



    
def date_query(request):
    income_amount_sum_list = Income.objects.filter(user = request.user).values("income").annotate(sum_products = Sum("income_amount")).order_by('income')

    incomeform = IncomeForm()
    income_instances_list = Income.objects.filter(user = request.user).values_list('income','income_instance_creation_date','income_amount')
    date_exceed = [(datetime.now(timezone.utc)- i[1]).days for i in income_instances_list]
    income_log_date_ago_tuple = list(zip(income_instances_list,date_exceed))[:5]

    current_user = request.user
    income_objects_before = Income.objects.filter(user = current_user)
    expense_objects = Expense.objects.filter(user = current_user)
    on_hand=on_hand_calc(income_objects_before,expense_objects)

    if request.method == "POST":
        date_string_start = request.POST["datetimestart"]
        datetime_object_start = datetime.strptime(date_string_start, '%Y-%m-%dT%H:%M')
        date_string_end = request.POST["datetimeend"]
        datetime_object_end = datetime.strptime(date_string_end, '%Y-%m-%dT%H:%M')
      
        income_objects = Income.objects.filter(user= current_user).filter(income_instance_creation_date__range=(datetime_object_start,datetime_object_end))
        return render(request, "IncomeExpenseCalc/income.html",{"incomeform":incomeform,"income_objects":income_objects,"income_log_date_ago_tuple":income_log_date_ago_tuple,"income_amount_sum_list":income_amount_sum_list,"on_hand":on_hand})
        


def income_report(request):
    return render(request, "IncomeExpenseCalc/incomereport.html")


def expense_report(request):
    if request.method == "POST":
        date_string_start = request.POST["datetimestart"]
        datetime_object_start = datetime.strptime(date_string_start, '%Y-%m-%dT%H:%M')
        date_string_end = request.POST["datetimeend"]
        datetime_object_end = datetime.strptime(date_string_end, '%Y-%m-%dT%H:%M')
        expense_objects = Expense.objects.filter(user= request.user).filter(expense_instance_creation_date__range=(datetime_object_start,datetime_object_end)).values("expense").annotate(sum_products = Sum("expense_amount")).order_by('expense')
        income_objects = Income.objects.filter(user= request.user).filter(income_instance_creation_date__range=(datetime_object_start,datetime_object_end)).values("income").annotate(sum_products = Sum("income_amount")).order_by('income')

        expense_sum = expense_objects.aggregate(Sum('expense_amount'))['expense_amount__sum']
        income_sum = income_objects.aggregate(Sum('income_amount'))['income_amount__sum']
        current_user = request.user
        income_objects_hand = Income.objects.filter(user = current_user)
        expense_objects_hand = Expense.objects.filter(user = current_user)
        on_hand=on_hand_calc(income_objects_hand,expense_objects_hand)
        #breakpoint()
        return render(request, "IncomeExpenseCalc/expensereport.html",{"expense_objects":expense_objects,"income_objects":income_objects,"expense_sum":expense_sum,"income_sum":income_sum,"on_hand":on_hand})
        
    return render(request, "IncomeExpenseCalc/expensereport.html")
    



