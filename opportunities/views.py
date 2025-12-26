from rest_framework import viewsets, permissions, filters
from .models import Opportunity
from .serializers import OpportunitySerializer
from .permissions import IsOrganizationOwner


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'location', 'description']

    def get_permissions(self):
        # Anyone can view
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]

        # Only logged-in orgs can create/update/delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrganizationOwner()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user)
