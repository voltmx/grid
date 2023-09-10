from django.conf import settings
from django.db import models
from django.db.models.functions import TruncDate
from django.contrib.postgres.fields import ArrayField
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Habit(BaseModel):
    user_id: models.UUIDField
    REGISTRY_TYPE_CHOICES = (
        ("numeric", "numeric"),
        ("time", "time"),
        ("boolean", "boolean"),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(choices=REGISTRY_TYPE_CHOICES, max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits"
    )
    units = models.CharField(blank=True, max_length=255)
    numeric_goal = models.IntegerField(null=True)
    days_of_week = ArrayField(models.CharField(max_length=3), default=list, blank=True)


class HabitEntry(BaseModel):
    habit_id: models.UUIDField
    date = models.DateField()
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="entries")
    description = models.TextField(
        blank=True,
    )
    completed = models.BooleanField(default=False)
    numerical = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint('date', 'habit', name="habit_date_unique"),
        ]
