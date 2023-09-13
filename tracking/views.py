from django.shortcuts import render
from rest_framework import generics
from tracking.models import Habit, HabitEntry
from django.db.models import Prefetch

from tracking.serializers import (
    HabitCreateSerializer,
    HabitEntryCreateSerializer,
    HabitEntryListRetrieveSerializer,
    HabitListRetrieveSerializer,
)

# //TODO Add permisions
# TODO Add authenthication requirement


class HabitListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return HabitCreateSerializer
        return HabitListRetrieveSerializer

    def get_queryset(self):
        qp = self.request.query_params
        date = qp.get("entry_date")
        user_id = self.request.user.id
        qs = Habit.objects.filter(user_id=user_id)
        if date:
            qs = qs.prefetch_related(
                Prefetch(
                    "entries",
                    queryset=HabitEntry.objects.filter(date=date),
                    to_attr="todays_entries",
                )
            )
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitListRetrieveSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Habit.objects.filter(user_id=user_id)


class HabitEntryListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return HabitEntryCreateSerializer
        return HabitEntryListRetrieveSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return HabitEntry.objects.filter(habit__user_id=user_id)
    
    def perform_create(self, serializer):
        print(repr(serializer))
        print(serializer.validated_data)
        return super().perform_create(serializer)


class HabitEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitEntryListRetrieveSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return HabitEntry.objects.filter(habit__user_id=user_id)
