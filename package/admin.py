from django.contrib import admin
from django.contrib.admin import register
from package.models import Package


@register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_active')
    list_filter = ('is_active',)
    actions = ('active_all',)

    def has_delete_permission(self, request, obj=None):
        return False
