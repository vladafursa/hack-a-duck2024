from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Teams
from .serializers import TeamsSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from employees.models import Employees
from employees.serializers import EmployeesSerializer
from .models import Teams
from django.core.exceptions import ValidationError
from django.shortcuts import render


@swagger_auto_schema(
    method='post',
    request_body=TeamsSerializer,
    responses={201: "User registered successfully!", 400: "Invalid data"}
)
@api_view(['POST'])
def create_team(request):
    serializer = TeamsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve all teams",
    responses={
        200: openapi.Response("A list of teams", TeamsSerializer(many=True)),
        400: "Bad Request",
    }
)
@api_view(['GET'])
def teams_list_view(request):
    teams = Teams.objects.all()
    serializer = TeamsSerializer(teams, many=True)
    return render(request, 'teams/teams.html', {'teams': serializer.data})

from django.shortcuts import render

from employees.views import get_ideal_team, get_actual_team, ask_chatgpt, get_preferred_team


def chosen_team(request, project):
    try:
        project_obj = Teams.objects.get(project=project)  # Get the project object

        # Call the get_ideal_team function to retrieve qualified employees
        qualified_employees_response = get_ideal_team(request, project_obj.project)

        # Extract employees from the response (assumed structure)
        if qualified_employees_response.status_code == 200:
            employees = qualified_employees_response.data
        else:
            employees = []  # or handle the error as needed

        return render(request, 'teams/chosen_team.html', {
            'project': project_obj,
            'Employees': employees,
        })
    except Teams.DoesNotExist:
        return render(request, '404.html')

def chosen_actual_team(request, project):
    try:
        project_obj = Teams.objects.get(project=project)  # Get the project object

        # Call the get_ideal_team function to retrieve qualified employees
        qualified_employees_response = get_actual_team(request, project_obj.project)

        # Extract employees from the response (assumed structure)
        if qualified_employees_response.status_code == 200:
            employees = qualified_employees_response.data
        else:
            employees = []  # or handle the error as needed

        return render(request, 'teams/chosen_team.html', {
            'project': project_obj,
            'Employees': employees,
        })
    except Teams.DoesNotExist:
        return render(request, '404.html')
def advice(request, project):
    try:
        project_obj = Teams.objects.get(project=project)  # Get the project object

        # Call the get_ideal_team function to retrieve qualified employees
        advice_response = ask_chatgpt(request, project_obj.project)



        return render(request, 'teams/chosen_team.html', {
            'project': project_obj,
            'advice': advice_response,
        })
    except Teams.DoesNotExist:
        return render(request, '404.html')


def preferred_team(request, project):
    try:
        project_obj = Teams.objects.get(project=project)  # Get the project object

        # Call the get_ideal_team function to retrieve qualified employees
        qualified_employees_response = get_ideal_team(request, project_obj.project)

        # Extract employees from the response (assumed structure)
        if qualified_employees_response.status_code == 200:
            employees = qualified_employees_response.data
            latest_availability = qualified_employees_response.data.get('latest_availability', None)
        else:
            employees = []  # or handle the error as needed
            latest_availability = None

        return render(request, 'teams/chosen_team.html', {
            'project': project_obj,
            'Employees': employees,
            'latest_availability': latest_availability,
        })
    except Teams.DoesNotExist:
        return render(request, '404.html')
