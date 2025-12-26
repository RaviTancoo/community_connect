from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsVolunteer
from notifications.models import Notification


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'volunteer':
            return Application.objects.filter(volunteer=user)
        return Application.objects.filter(opportunity__organization=user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsVolunteer()]
        return super().get_permissions()

    def perform_create(self, serializer):
        application = serializer.save(volunteer=self.request.user)

        # Notify the organization
        Notification.objects.create(
            user=application.opportunity.organization,
            message=f"{self.request.user.username} applied to {application.opportunity.title}"
        )

    def perform_update(self, serializer):
        user = self.request.user
        app = serializer.instance
        data = serializer.validated_data

        if user.user_type == 'organization':
            # Org can update hours_logged and feedback
            if 'hours_logged' in data:
                app.hours_logged = data['hours_logged']
            if 'feedback' in data:
                app.feedback = data['feedback']
            app.save()
        else:
            # Volunteers cannot update hours or feedback
            allowed_fields = ['status']  # Only fields volunteers can update, adjust if needed
            for field in allowed_fields:
                if field in data:
                    setattr(app, field, data[field])
            app.save()

    # Optional: separate endpoints for logging hours and adding feedback
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def log_hours(self, request, pk=None):
        app = self.get_object()
        if request.user != app.opportunity.organization:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        hours = request.data.get('hours_logged')
        if hours is not None:
            app.hours_logged = hours
            app.save()
            return Response({"hours_logged": app.hours_logged})
        return Response({"detail": "No hours provided"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def add_feedback(self, request, pk=None):
        app = self.get_object()
        if request.user != app.opportunity.organization:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        feedback = request.data.get('feedback')
        if feedback is not None:
            app.feedback = feedback
            app.save()
            return Response({"feedback": app.feedback})
        return Response({"detail": "No feedback provided"}, status=status.HTTP_400_BAD_REQUEST)
