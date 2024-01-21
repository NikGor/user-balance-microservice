from django.contrib import admin
from UserBalanceMicroservice.orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'service')
    search_fields = ('user__username', 'service__name')


admin.site.register(Order, OrderAdmin)
