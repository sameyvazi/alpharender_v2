from django.contrib import admin
from django.contrib.admin import register
from transaction.models import Transaction, UserBalance


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount']

    search_fields = ['user']
    list_display_links = ['id', 'user']


@register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance']

    search_fields = ['user']
    list_display_links = ['id', 'user']
