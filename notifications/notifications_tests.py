import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from notifications.models import Notification
from opportunities.models import Opportunity

User = get_user_model()


@pytest.mark.django_db
class TestNotifications:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def volunteer(self):
        return User.objects.create_user(
            username="volunteer1",
            email="volunteer@test.com",
            password="password123",
            user_type="volunteer"
        )

    @pytest.fixture
    def organization(self):
        return User.objects.create_user(
            username="org1",
            email="org@test.com",
            password="password123",
            user_type="organization"
        )

    @pytest.fixture
    def opportunity(self, organization):
        return Opportunity.objects.create(
            title="Beach Cleanup",
            description="Help clean the beach",
            organization=organization,
            location="Port of Spain",
            required_skills="Teamwork",
            start_date="2025-01-01",
            end_date="2025-01-02"
        )

    @pytest.fixture(autouse=True)
    def clear_notifications(self):
        Notification.objects.all().delete()

    def test_notification_created_on_application(self, client, volunteer, opportunity):
        client.force_authenticate(user=volunteer)

        response = client.post(
            "/api/applications/",
            {"opportunity": opportunity.id}
        )

        assert response.status_code == 201

        notifications = Notification.objects.filter(user=opportunity.organization)
        assert notifications.count() == 1

        notification = notifications.first()
        assert "applied" in notification.message.lower()

    def test_user_can_view_own_notifications(self, client, volunteer, opportunity):
        # Create notification manually
        Notification.objects.create(
            user=volunteer,
            message="Test notification"
        )

        client.force_authenticate(user=volunteer)
        response = client.get("/api/notifications/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["message"] == "Test notification"

    def test_user_cannot_see_other_users_notifications(self, client, volunteer, organization):
        Notification.objects.create(
            user=organization,
            message="Org notification"
        )

        client.force_authenticate(user=volunteer)
        response = client.get("/api/notifications/")

        assert response.status_code == 200
        assert len(response.data) == 0
