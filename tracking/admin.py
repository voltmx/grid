from django.contrib import admin

# Register your models here.
# Admin site for tracking.models
from tracking.models import Habit, HabitEntry


# Inline for HabitAdmin
class HabitEntryInline(admin.TabularInline):
    model = HabitEntry
    extra = 1
    fields = ('date', 'description', 'completed', 'numerical')

class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user', 'units', 'numeric_goal', 'days_of_week')
    list_filter = ('type', 'user', 'days_of_week')
    search_fields = ('name', 'user__email', 'days_of_week')
    inlines = [
        HabitEntryInline,
    ]

class HabitEntryAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'description', 'completed', 'numerical')
    list_filter = ('habit', 'date', 'completed')
    search_fields = ('habit__name', 'date', 'description', 'completed', 'numerical')


admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitEntry, HabitEntryAdmin)

