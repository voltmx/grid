from django_filters import rest_framework as filters

from tracking.models import Habit, HabitEntry

class UuidInFilter(filters.BaseInFilter, filters.UUIDFilter):
    pass

class HabitEntryFilter(filters.FilterSet):
    date__gte = filters.DateFilter(field_name='date', lookup_expr='gte')
    date__lte = filters.DateFilter(field_name='date', lookup_expr='lte')
    habit_id__in = UuidInFilter(field_name='habit_id', lookup_expr='in')
    class Meta:
        model = HabitEntry
        fields = ['habit_id', 'date']

class HabitFilter(filters.FilterSet):
    class Meta:
        model = Habit
        fields = ['user_id', 'is_archived']