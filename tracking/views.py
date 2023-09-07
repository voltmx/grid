from django.shortcuts import render
from rest_framework import generics
from tracking.models import Habit, HabitEntry

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
        user_id = self.request.user.id
        return Habit.objects.filter(user_id=user_id)
    
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


class HabitEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitEntryListRetrieveSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return HabitEntry.objects.filter(habit__user_id=user_id)
