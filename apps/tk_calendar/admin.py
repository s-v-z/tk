from django.contrib import admin
from apps.tk_calendar.models import Category, Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)