from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from opportunities.models import Opportunity

User = get_user_model()


class TestOpportunities(APITestCase):

    def setUp(self):
        self.org_user = User.objects.create_user(
            username="org1",
            password="password123",
            user_type="organization"
        )

        self.other_org = User.objects.create_user(
            username="org2",
            password="password123",
            user_type="organization"
        )

        self.volunteer = User.objects.create_user(
            username="volunteer1",
            password="password123",
            user_type="volunteer"
        )

        self.opportunity = Opportunity.objects.create(
            title="Beach Cleanup",
            description="Clean the beach",
            location="Port of Spain",
            required_skills="Teamwork",
            start_date="2025-12-20",
            end_date="2025-12-21",
            organization=self.org_user
        )

        self.list_url = reverse("opportunity-list")
        self.detail_url = reverse("opportunity-detail", args=[self.opportunity.id])

    # ----------------------------
    # LIST
    # ----------------------------
    def test_anyone_can_view_opportunities(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ----------------------------
    # CREATE
    # ----------------------------
    def test_organization_can_create_opportunity(self):
        self.client.force_authenticate(user=self.org_user)

        data = {
            "title": "Tree Planting",
            "description": "Plant trees",
            "location": "San Fernando",
            "required_skills": "Teamwork",
            "start_date": "2025-12-22",
            "end_date": "2025-12-23"
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_volunteer_cannot_create_opportunity(self):
        self.client.force_authenticate(user=self.volunteer)

        data = {
            "title": "Illegal",
            "description": "Nope",
            "location": "Nowhere",
            "required_skills": "None",
            "start_date": "2025-12-22",
            "end_date": "2025-12-23"
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------
    # UPDATE
    # ----------------------------
    def test_organization_can_update_own_opportunity(self):
        self.client.force_authenticate(user=self.org_user)

        response = self.client.patch(
            self.detail_url,
            {"location": "San Fernando"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_org_cannot_update_opportunity(self):
        self.client.force_authenticate(user=self.other_org)

        response = self.client.patch(
            self.detail_url,
            {"location": "Arima"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_volunteer_cannot_update_opportunity(self):
        self.client.force_authenticate(user=self.volunteer)

        response = self.client.patch(
            self.detail_url,
            {"location": "Arima"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------
    # DELETE
    # ----------------------------
    def test_organization_can_delete_opportunity(self):
        self.client.force_authenticate(user=self.org_user)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_volunteer_cannot_delete_opportunity(self):
        self.client.force_authenticate(user=self.volunteer)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
