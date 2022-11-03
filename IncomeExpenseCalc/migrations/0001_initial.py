# Generated by Django 4.1.2 on 2022-11-02 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('income_id', models.IntegerField(primary_key=True, serialize=False)),
                ('income', models.CharField(choices=[('salary', 'salary'), ('Investments', 'Investments'), ('Rental', 'Rental')], max_length=100)),
                ('income_instance_creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation date')),
                ('income_amount', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Income data',
                'ordering': ['-income_instance_creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('expense_id', models.IntegerField(primary_key=True, serialize=False)),
                ('expense', models.CharField(choices=[('Housing rent', 'Housing rent'), ('Transportation', 'Transportation'), ('Food and groceries', 'Food and groceries'), ('Utility bills', 'Utility bills')], max_length=100)),
                ('expense_instance_creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation date')),
                ('expense_amount', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'expense data',
                'ordering': ['-expense_instance_creation_date'],
            },
        ),
    ]