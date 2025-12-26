import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from opportunities.models import Opportunity
from applications.models import Application
from notifications.models import Notification

User = get_user_model()

@pytest.mark.django_db
class TestApplications:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def volunteer(self):
        return User.objects.create_user(
            username="volunteer1",
            email="volunteer1@example.com",
            password="password123",
            user_type="volunteer"
        )

    @pytest.fixture
    def organization(self):
        return User.objects.create_user(
            username="org1",
            email="org1@example.com",
            password="password123",
            user_type="organization"
        )

    @pytest.fixture
    def opportunity(self, organization):
        return Opportunity.objects.create(
            title="Beach Cleanup",
            description="Clean the beach",
            organization=organization,
            location="Siparia",
            required_skills="Teamwork",
            start_date="2025-12-20",
            end_date="2025-12-21"
        )

    def test_volunteer_can_apply(self, client, volunteer, opportunity):
        client.force_authenticate(user=volunteer)
        url = reverse('application-list')
        data = {"opportunity": opportunity.id}

        response = client.post(url, data)
        assert response.status_code == 201

        app = Application.objects.get(volunteer=volunteer, opportunity=opportunity)
        assert app.status == 'pending'

        # Notification created
        notif = Notification.objects.filter(user=opportunity.organization).last()
        assert f"{volunteer.username} applied to {opportunity.title}" in notif.message

    def test_volunteer_cannot_apply_twice(self, client, volunteer, opportunity):
        client.force_authenticate(user=volunteer)
        Application.objects.create(volunteer=volunteer, opportunity=opportunity)
        url = reverse('application-list')
        data = {"opportunity": opportunity.id}

        response = client.post(url, data)
        assert response.status_code == 400
        assert "already applied" in response.data['non_field_errors'][0]

    def test_organization_can_update_hours(self, client, organization, volunteer, opportunity):
        app = Application.objects.create(volunteer=volunteer, opportunity=opportunity)
        client.force_authenticate(user=organization)

        url = reverse('application-detail', args=[app.id])
        response = client.patch(url, {"hours_logged": 5})
        assert response.status_code == 200

        app.refresh_from_db()
        assert app.hours_logged == 5

    def test_organization_can_update_feedback(self, client, organization, volunteer, opportunity):
        app = Application.objects.create(volunteer=volunteer, opportunity=opportunity)
        client.force_authenticate(user=organization)

        url = reverse('application-detail', args=[app.id])
        response = client.patch(url, {"feedback": "Great work!"})
        assert response.status_code == 200

        app.refresh_from_db()
        assert app.feedback == "Great work!"

    def test_volunteer_cannot_update_hours_or_feedback(self, client, volunteer, opportunity):
        app = Application.objects.create(volunteer=volunteer, opportunity=opportunity)
        client.force_authenticate(user=volunteer)

        url = reverse('application-detail', args=[app.id])
        response = client.patch(url, {"hours_logged": 10, "feedback": "Awesome!"})
        assert response.status_code == 200

        app.refresh_from_db()
        # Fields remain unchanged
        assert app.hours_logged == 0
        assert app.feedback == ""
