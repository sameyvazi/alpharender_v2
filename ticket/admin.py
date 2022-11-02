from django.contrib import admin
from django.contrib.admin import register

from ticket.models import Department, Reply, Ticket


@register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    actions = ('active_all',)

    def active_all(self, request, queryset):
        pass

    def has_delete_permission(self, request, obj=None):
        return False


@register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'department_id', 'subject', 'status']
    list_filter = ['status', 'department_id__title']
    search_fields = ['id', 'title']
    list_display_links = ['id', 'subject']
