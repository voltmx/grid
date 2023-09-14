from django.test import TestCase
from django.urls import reverse

from tracking.models import Habit, HabitEntry
from users.models import User

# Create your tests here.
class HabitListCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email="test@test.com")
        self.user_2 = User.objects.create_user(email="test2@test.com")
        self.habit = Habit.objects.create(user=self.user, name="test habit", type="boolean")
        self.habit_2 = Habit.objects.create(user=self.user, name="test2 habit", type="boolean", is_public=True)
        self.entry = HabitEntry.objects.create(habit=self.habit, date="2021-01-01")
        self.url = reverse("habit-list")
        return super().setUp()
    
    def test_retrieve(self):
        """
        Ensure user can list all their habits
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "test habit")
        self.assertEqual(data[0]["id"], str(self.habit.id))
        # Test that today_entries is not added if no entry_date query param is passed
        self.assertEqual(data[0].get("today_entries"), None)

        # Test that adding entry_date query param returns todays_entries
        response = self.client.get(self.url+"?entry_date=2021-01-01")
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], str(self.habit.id))
        
        self.assertEqual(data[0]["name"], "test habit")
        self.assertEqual(len(data[0]["today_entries"]), 1)
        self.assertEqual(data[0]["today_entries"][0]["date"], "2021-01-01")
        self.assertEqual(data[0]["today_entries"][0]["id"], str(self.entry.id))

    def test_user_can_see_public_habits(self):
        """
        Ensure user can see public habits from other users, not private ones
        """
        self.client.force_login(self.user_2)
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "test2 habit")

    def test_create(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={"name": "test habit 2", "type": "boolean"})
        data = response.json()
        self.assertEqual(data["name"], "test habit 2")
        self.assertEqual(data["type"], "boolean")
        self.assertEqual(data["user_id"], str(self.user.id))
        self.assertEqual(data["days_of_week"], [])
        self.assertEqual(data["units"], "")
        self.assertEqual(data["numeric_goal"], None)
        self.assertEqual(data["id"], str(Habit.objects.get(name="test habit 2").id))