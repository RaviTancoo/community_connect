from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['volunteer', 'applied_at']

    def validate(self, data):
        """
        Validate application creation and prevent duplicates.
        """
        user = self.context['request'].user
        opportunity = data.get('opportunity')  # safe for partial updates

        # On create, opportunity must be provided
        if self.instance is None and not opportunity:
            raise serializers.ValidationError({'opportunity': 'This field is required.'})

        # Prevent duplicate applications
        if opportunity and Application.objects.filter(volunteer=user, opportunity=opportunity).exists():
            raise serializers.ValidationError("You have already applied to this opportunity.")

        return data

    def update(self, instance, validated_data):
        """
        Handle partial updates: 
        - Volunteers can update hours and hours_logged
        - Organizations can update feedback and status
        """
        user = self.context['request'].user

        # Volunteers can only update hours fields
        if user.user_type == 'volunteer':
            instance.hours = validated_data.get('hours', instance.hours)
            instance.hours_logged = validated_data.get('hours_logged', instance.hours_logged)

        # Organizations can only update feedback and status
        elif user.user_type == 'organization':
            instance.feedback = validated_data.get('feedback', instance.feedback)
            instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance

