from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("user/",views.user,name="user"),
    path("user/income/",views.new_income,name="income"),
    path("user/expense/",views.new_expense,name="expense"),
    path("onhand/",views.on_hand_calc,name="onhand"),

]

