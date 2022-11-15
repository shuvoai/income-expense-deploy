from ast import Is
from .models import *
from matplotlib import pyplot as plt
import io, base64


def on_hand_calc(income_objects,expense_objects):
    income_amount = 0
    for i in  income_objects:
        income_amount = i.income_amount+income_amount
    expense_amount = 0
    for i in  expense_objects:
        expense_amount = i.expense_amount+expense_amount
    on_hand = income_amount - expense_amount
    
    return on_hand


def pie_chart(objList):
    labels= []
    amount = []

    for i in objList:
        for value in i.values():
            if type(value) == str:
                labels.append(value)
            elif type(value) == int:
                amount.append(value)           

    return labels,amount


def pie_chart_plot(income_amount_sum_list,expense_amount_sum_list):
    
    
    expense_names,expense_amounts = pie_chart(expense_amount_sum_list)
    income_names, income_amounts = pie_chart(income_amount_sum_list)

    fig,axs = plt.subplots(2, 1, figsize=(6, 6))

    axs[0].pie(income_amounts,labels = income_names,shadow = True,autopct='%1.1f%%')
    axs[0].set_title("Income Pie Chart")
    
    axs[1].pie(expense_amounts,labels = expense_names,shadow = True,autopct='%1.1f%%')
    axs[1].set_title("Expense Pie Chart")
    plt.axis('equal')

    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    return b64




