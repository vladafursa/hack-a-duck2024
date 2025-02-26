# Register your models here.
from rest_framework import serializers
from .models import Employees
import django_filters
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ["name", "email", "skills", "experience", "location", "type_of_work", "availability", "security_clearance", "temperament"]


class FilteredEmployeesSerializer(django_filters.FilterSet):
    class Meta:
        model = Employees
        fields = ["name", "email", "skills", "experience", "location", "type_of_work", "availability",
                  "security_clearance", "temperament"]


class ChatRequestSerializer(serializers.Serializer):
    employees = serializers.ListField(
        child=EmployeesSerializer(),
        allow_empty=False
    )

