from rest_framework import serializers

from tracking.models import Habit, HabitEntry


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ["name", "days_of_week", "type", "units", "numeric_goal"]


class HabitListRetrieveSerializer(serializers.ModelSerializer):
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
            "user",
        ]


class HabitEntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitEntry
        fields = [
            "habit",
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
            "habit",
            "date",
            "description",
            "completed",
            "numerical",
        ]
