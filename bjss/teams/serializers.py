# Register your models here.
from rest_framework import serializers
from .models import Teams

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ["project", "required_skills", "location", "type_of_work", "start_date", "type_of_work", "security_clearance", "team_size", "experience"]


