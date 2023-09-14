from django.shortcuts import render
from rest_framework import generics
from tracking.models import Habit, HabitEntry
from django.db.models import Prefetch, Q

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
        # User can only see their own habits, unless they are public
        public_habit_q = Q(is_public=True)
        user_habit_q = Q(user_id=user_id)

        qs = Habit.objects.filter(public_habit_q | user_habit_q)

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
        # User can only see their own habits, unless they are public
        public_habit_q = Q(is_public=True)
        user_habit_q = Q(user_id=user_id)
        qs = Habit.objects.filter(public_habit_q | user_habit_q)
        return qs


class HabitEntryListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return HabitEntryCreateSerializer
        return HabitEntryListRetrieveSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        # User can only see their own habits, unless they are public
        public_habit_q = Q(habit__is_public=True)
        user_habit_q = Q(habit__user_id=user_id)
        qs = HabitEntry.objects.filter(public_habit_q | user_habit_q)
        return qs
    
    def perform_create(self, serializer):
        print(repr(serializer))
        print(serializer.validated_data)
        return super().perform_create(serializer)


class HabitEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitEntryListRetrieveSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        # User can only see their own habits, unless they are public
        public_habit_q = Q(habit__is_public=True)
        user_habit_q = Q(habit__user_id=user_id)
        qs = HabitEntry.objects.filter(public_habit_q | user_habit_q)
        return qs