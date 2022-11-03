from django.contrib import admin

# Register your models here.
from .models import Income, Expense


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["user","income","income_instance_creation_date","income_amount"]

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["user","expense","expense_instance_creation_date","expense_amount"]
