import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserAuth:

    @pytest.fixture
    def client(self):
        return APIClient()

    # Registration Test
    def test_user_can_register(self, client):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "user_type": "volunteer",
            "location": "NYC"
        }
        response = client.post(url, data)
        assert response.status_code == 201
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert user.user_type == "volunteer"

    # LOGIN [VALID CREDENTIALS]
    def test_user_can_login(self, client):
        User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            user_type="volunteer"
        )
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert "access" in response.data

    # LOGIN [INVALID CREDENTIALS]
    def test_user_cannot_login_with_wrong_credentials(self, client):
        User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            user_type="volunteer"
        )
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post(url, data)
        assert response.status_code == 401
        assert "access" not in response.data

    # PROFILE VIEW.
    def test_user_can_view_profile(self, client):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            user_type="volunteer"
        )
        client.force_authenticate(user=user)
        url = reverse('profile')
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["username"] == "testuser"
        assert response.data["email"] == "testuser@example.com"
        assert response.data["user_type"] == "volunteer"

    # PROFILE UPDATE.
    def test_user_can_update_profile(self, client):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            user_type="volunteer",
            location="Old Location"
        )
        client.force_authenticate(user=user)
        url = reverse('profile')
        response = client.patch(url, {"location": "New Location"})
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.location == "New Location"
