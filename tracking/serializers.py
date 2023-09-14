from rest_framework import serializers

from tracking.models import Habit, HabitEntry


class HabitEntryCreateSerializer(serializers.ModelSerializer):
    habit_id = serializers.PrimaryKeyRelatedField(source="habit", queryset=Habit.objects.all())
    class Meta:
        model = HabitEntry
        fields = [
            "id",
            "habit_id",
            "date",
            "description",
            "completed",
            "numerical",
        ]


class HabitEntryListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitEntry
        fields = [
            "id",
            "created_at",
            "edited_at",
            "habit_id",
            "date",
            "description",
            "completed",
            "numerical",
        ]
        read_only_fields = [
            "habit_id",
            "created_at",
            "edited_at",
            "date"
        ]


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "name",
            "days_of_week",
            "type",
            "units",
            "numeric_goal",
            "user_id",
            "created_at",
            "edited_at",
            "is_archived"
        ]
        read_only_fields = [
            "user_id",
            "created_at",
            "edited_at",
        ]


class HabitListRetrieveSerializer(serializers.ModelSerializer):
    today_entries = HabitEntryListRetrieveSerializer(
        read_only=True, many=True, source="todays_entries"
    )

    class Meta:
        model = Habit
        fields = [
            "id",
            "created_at",
            "edited_at",
            "units",
            "days_of_week",
            "name",
            "type",
            "user_id",
            "today_entries",
            "numeric_goal",
            "is_archived"
        ]
