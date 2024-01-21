# transactions/admin.py
from django.contrib import admin
from UserBalanceMicroservice.transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'created_at', 'status')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'comment')
    date_hierarchy = 'created_at'


admin.site.register(Transaction, TransactionAdmin)
