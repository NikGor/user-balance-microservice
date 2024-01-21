# user_accounts/admin.py
from django.contrib import admin
from UserBalanceMicroservice.user_accounts.models import AccountBalance


class AccountBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user',)


admin.site.register(AccountBalance, AccountBalanceAdmin)
