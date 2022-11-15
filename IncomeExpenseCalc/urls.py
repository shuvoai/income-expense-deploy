from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path("user/",views.user,name="userpre"),
    path("user/income/",views.income,name="income"),
    path("user/expense/",views.expense,name="expense"),
    path("user/incomepage/",views.income, name="incomepage" ),
    path("user/expensepage/",views.expense, name="expensepage" ),
    path("user/date_query/",views.date_query, name="datesearch" ),
    path("user/incomereport/",views.income_report, name="incomereport" ),
    path("user/expensereport/",views.expense_report, name="expensereport" ),

]

