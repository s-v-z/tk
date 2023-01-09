from django.contrib import admin
from apps.tk_database.models import Hike, HikeType, GeoRegion, CalendarEvent, UserProfile

# Register your models here.
class HikeAdmin(admin.ModelAdmin):
    pass

class HikeTypeAdmin(admin.ModelAdmin):
    pass

class GeoRegionAdmin(admin.ModelAdmin):
    pass

class CalendarEventAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hike, HikeAdmin)
admin.site.register(HikeType, HikeTypeAdmin)
admin.site.register(GeoRegion, GeoRegionAdmin)
admin.site.register(CalendarEvent, CalendarEventAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
