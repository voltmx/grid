from django.urls import path
from .views import (
    HabitListCreateView,
    HabitDetailView,
    HabitEntryListCreateView,
    HabitEntryDetailView,
)

urlpatterns = [
    # Habit endpoints
    path("habits/", HabitListCreateView.as_view(), name="habit-list"),
    path("habits/<uuid:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    # HabitEntry endpoints
    path("habit-entries/", HabitEntryListCreateView.as_view(), name="habitentry-list"),
    path(
        "habit-entries/<uuid:pk>/",
        HabitEntryDetailView.as_view(),
        name="habitentry-detail",
    ),
]
