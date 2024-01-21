from django.contrib import admin
from UserBalanceMicroservice.services.models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


admin.site.register(Service, ServiceAdmin)
