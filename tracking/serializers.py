from rest_framework import serializers

from tracking.models import Habit, HabitEntry


class HabitEntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitEntry
        fields = [
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
        ]
