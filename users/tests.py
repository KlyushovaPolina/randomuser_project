from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json
from .models import User

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('requests.get')
    def test_index_post_loads_users_from_api(self, mock_get):
        # Мокаем ответ от randomuser.me
        mock_response_data = {
            "results": [
                {
                    "gender": "male",
                    "name": {"first": "John", "last": "Doe"},
                    "phone": "123-456-7890",
                    "email": "john.doe@example.com",
                    "location": {"city": "CityA", "country": "CountryA"},
                    "picture": {"thumbnail": "http://example.com/pic.jpg"}
                },
                {
                    "gender": "female",
                    "name": {"first": "Jane", "last": "Smith"},
                    "phone": "987-654-3210",
                    "email": "jane.smith@example.com",
                    "location": {"city": "CityB", "country": "CountryB"},
                    "picture": {"thumbnail": "http://example.com/pic2.jpg"}
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        # Отправляем POST запрос с count=2
        response = self.client.post(reverse('index'), data={'count': 2})
        self.assertEqual(response.status_code, 302)  # redirect после загрузки

        # Проверяем, что в базе появились 2 пользователя
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

        user1 = users[0]
        self.assertEqual(user1.first_name, "John")
        self.assertEqual(user1.gender, "male")

        user2 = users[1]
        self.assertEqual(user2.first_name, "Jane")
        self.assertEqual(user2.gender, "female")

    def test_index_get_shows_users(self):
        # Создаем пользователей в БД
        User.objects.create(
            gender="male", first_name="Test", last_name="User",
            phone="111-222", email="test@example.com",
            location="City, Country", picture="http://example.com/pic.jpg"
        )

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")
        self.assertContains(response, "User")

    def test_user_detail_view(self):
        user = User.objects.create(
            gender="female", first_name="Alice", last_name="Wonderland",
            phone="555-666", email="alice@example.com",
            location="Wonder City", picture="http://example.com/alice.jpg"
        )
        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
        self.assertContains(response, "Wonderland")

    def test_random_user_view(self):
        # Создаем нескольких пользователей
        User.objects.create(
            gender="male", first_name="Bob", last_name="Builder",
            phone="111-333", email="bob@example.com",
            location="Build City", picture="http://example.com/bob.jpg"
        )
        User.objects.create(
            gender="female", first_name="Carol", last_name="Singer",
            phone="222-444", email="carol@example.com",
            location="Sing City", picture="http://example.com/carol.jpg"
        )

        response = self.client.get(reverse('random-user'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть имя одного из созданных пользователей
        content = response.content.decode()
        self.assertTrue("Bob" in content or "Carol" in content)

    def test_random_user_view_no_users(self):
        # Если пользователей в базе нет, возвращается ошибка
        response = self.client.get(reverse('random-user'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No users in DB")
