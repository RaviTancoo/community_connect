from rest_framework import serializers
from .models import Opportunity

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = [
            'id',
            'title',
            'description',
            'organization',
            'location',
            'latitude',
            'longitude',
            'required_skills',
            'start_date',
            'end_date',
            'created_at',
        ]
        read_only_fields = ['organization', 'latitude', 'longitude', 'created_at']
