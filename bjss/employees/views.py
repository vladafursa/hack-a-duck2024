from .models import Employees
from .serializers import EmployeesSerializer, FilteredEmployeesSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from distutils.util import strtobool
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import openai
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import openai
from teams.models import Teams
from django.shortcuts import render, redirect




def employees_list_view(request):
    employees = Employees.objects.all().order_by('-experience')  # Retrieve and order employees
    context = {
        'Employees': employees,  # Pass the employee queryset to the template
    }
    return render(request, 'employees/employees.html', context)


@swagger_auto_schema(
    method='post',
    request_body=EmployeesSerializer,
    responses={201: "User registered successfully!", 400: "Invalid data"}
)
@api_view(['POST'])
def create_employee(request):
    serializer = EmployeesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name="skills",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Comma-separated list of skills to filter employees by (must include all specified skills).",
            required=True
                ),
        openapi.Parameter(
            name="experience",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            format=openapi.FORMAT_INT64,
            description="Specify the minimal experience in years",
            required=True,
        ),
        openapi.Parameter(
            name="availability",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE,
            description="Specify the start date to availability from (YYYY-MM-DD).",
            required=True,
        ),
        openapi.Parameter(
            name="location",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Specify the location of the employee.",
            required=True,
        ),
        openapi.Parameter(
            name="type_of_work",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_BOOLEAN,
            description="Filter by type of work: if the employee is able to work on projects on ethical grounds",
            required=True,
        ),
        openapi.Parameter(
            name="security_clearance",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_BOOLEAN,
            description="Specify if the employee has security clearance",
            required=True,
        ),
        openapi.Parameter(
            name="temperament",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Specify the temperament of the employee.",
            required=True,
        ),
    ],
    responses={
        200: openapi.Response("Filtered Employees retrieved successfully", EmployeesSerializer(many=True)),
        400: "Invalid parameter value",
    },
)
@api_view(['GET'])
def filtered_employees_list_view(request):
    employees = Employees.objects.all()
    try:
        # Retrieve parameters directly
        skills_param = request.GET.get('skills', '')
        available_since = request.GET.get('availability', '')
        minimal_experience = request.GET.get('experience', 0)
        retrieved_location = request.GET.get('location', '')
        retrieved_type_of_work = bool(strtobool(request.GET.get('type_of_work', '')))
        retrieved_security_clearance = bool(strtobool(request.GET.get('security_clearance', '')))
        retrieved_temperament = request.GET.get('temperament', '')

        # Filter by skills
        if skills_param:
            skills_list = [skill.strip() for skill in skills_param.split(',')]
            skills_query = Q()
            for skill in skills_list:
                skills_query &= Q(skills__icontains=skill)  # Ensuring each skill must be included
            employees = employees.filter(skills_query).distinct()

        # Apply additional filters
        employees = employees.filter(
            availability__lte=available_since,
            experience__gte=minimal_experience,
            location=retrieved_location,
            type_of_work=retrieved_type_of_work,
            security_clearance=retrieved_security_clearance,
            temperament=retrieved_temperament,
        )
        employees = employees.order_by('-experience')
        serializer = EmployeesSerializer(employees, many=True)
        return render(request, 'employees/employees.html', {'Employees': employees})

    except ValueError as e:
        raise ValidationError(f"Invalid parameter value: {e}")


def calculate_best_team(employees, required_skills):
    qualified_employees = []

    # Ensure required_skills is processed as a set for faster operations
    required_skills = set(required_skills)

    while required_skills:
        best_employee = None
        max_matching_skills = 0

        for employee in employees:
            employee_skills = set(skill.strip() for skill in employee.skills.split(','))  # Use a set for employee skills
            matching_skills = len(required_skills.intersection(employee_skills))  # Count matching skills using set intersection

            # Update best_employee if this one has more matching skills
            if matching_skills > max_matching_skills:
                best_employee = employee
                max_matching_skills = matching_skills
            # If matching skills are equal, prefer the one with more experience
            elif matching_skills == max_matching_skills and best_employee is not None:
                if employee.experience > best_employee.experience:
                    best_employee = employee

        # If a best employee was found
        if best_employee:
            qualified_employees.append(best_employee)

            # Remove matching skills from required_skills
            employee_skills = set(skill.strip() for skill in best_employee.skills.split(','))
            required_skills.difference_update(employee_skills)  # Remove matched skills

            # Exclude the best_employee from the next iteration
            employees = [emp for emp in employees if emp != best_employee]
        else:
            break  # Break if no best employee is found

    return qualified_employees


def filter_employees(team_id):
    try:
        # Retrieve the team and its associated project requirements
        team = Teams.objects.get(project=team_id)


        # Extract project requirements
        minimal_experience = team.experience  # Assuming you have this field in your Project model
        retrieved_location = team.location
        retrieved_type_of_work = team.type_of_work
        retrieved_security_clearance = team.security_clearance

        # Get all employees and apply filtering based on project requirements
        employees = Employees.objects.filter(
            experience__gte=minimal_experience,
            location=retrieved_location,
            type_of_work=retrieved_type_of_work,
            security_clearance=retrieved_security_clearance,
        ).order_by('-experience')  # Order by experience descending

        return employees  # Return the filtered queryset

    except Teams.DoesNotExist:
        raise ValidationError("Team not found")
    except Exception as e:
        raise ValidationError(f"An error occurred: {e}")


@api_view(['GET'])
def filtered_team_list_view(request, project):
    try:
        employees = filter_employees(project)  # Call the filtering function with team_id

        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name="project",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="Specify the ID of the team to filter employees",
            required=True,
        ),
    ],
    responses={
        200: openapi.Response("Filtered Employees retrieved successfully", EmployeesSerializer(many=True)),
        400: "Invalid parameter value or team not found",
    },
)
@api_view(['GET'])
def get_ideal_team(request, project):
    try:
        employees = filter_employees(project)  # Use the same filtering function
        team = Teams.objects.get(project=project)



        required_skills =  [skill.strip().strip('"') for skill in team.required_skills.split(',')]

        print(required_skills)
        qualified_employees = calculate_best_team(employees, required_skills)

        serializer = EmployeesSerializer(qualified_employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




def filter_actual_employees(team_id):
    try:
        team = Teams.objects.get(project=team_id)
        minimal_experience = team.experience  # Assuming you have this field in your Project model
        retrieved_location = team.location
        retrieved_type_of_work = team.type_of_work
        retrieved_security_clearance = team.security_clearance
        available_since = team.start_date
        # Apply filtering
        employees = Employees.objects.filter(
            availability__lte=available_since,
            experience__gte=minimal_experience,
            location=retrieved_location,
            type_of_work=retrieved_type_of_work,
            security_clearance=retrieved_security_clearance,
        ).order_by('-experience')  # Order by experience descending

        return employees  # Return the filtered queryset

    except ValueError as e:
        raise ValidationError(f"Invalid parameter value: {e}")


@api_view(['GET'])
def filter_actual_employees_list_view(request, project):
    try:
        employees = filter_actual_employees(project)

        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name="project",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="Specify the ID of the team to filter employees",
            required=True,
        ),
    ],
    responses={
        200: openapi.Response("Filtered Employees retrieved successfully", EmployeesSerializer(many=True)),
        400: "Invalid parameter value or team not found",
    },
)
@api_view(['GET'])
def get_actual_team(request, project):
    try:
        employees = filter_actual_employees(project)  # Use the same filtering function
        team = Teams.objects.get(project=project)

        required_skills = [skill.strip().strip('"') for skill in team.required_skills.split(',')]

        qualified_employees = calculate_best_team(employees, required_skills)  # Call your calculation logic

        serializer = EmployeesSerializer(qualified_employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)







from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response

def filter_preferred_employees(request, team_id):
    try:
        team = Teams.objects.get(project=team_id)
        minimal_experience = team.experience
        retrieved_location = team.location
        retrieved_type_of_work = team.type_of_work
        retrieved_security_clearance = team.security_clearance
        available_since = team.start_date  # This should be a date object already

        # Apply filtering
        duration = int(request.GET.get('duration', 0))  # Duration in days or months
        unit = request.GET.get('unit', 'days')  # Specify if it's in days or months

        # Calculate the date to filter based on duration and unit
        if unit == 'days':
            filter_date = available_since + timedelta(days=duration)
        elif unit == 'months':
            filter_date = available_since + relativedelta(months=duration)
        else:
            raise ValidationError("Invalid unit specified. Use 'days' or 'months'.")

        # Apply filtering
        employees = Employees.objects.filter(
            availability__lte=filter_date,
            experience__gte=minimal_experience,
            location=retrieved_location,
            type_of_work=retrieved_type_of_work,
            security_clearance=retrieved_security_clearance,
        ).order_by('-experience')  # Order by experience descending

        return employees  # Return the filtered queryset

    except ValueError as e:
        raise ValidationError(f"Invalid parameter value: {e}")

@api_view(['GET'])
def filter_preferred_employees_list_view(request, project):
    try:
        employees = filter_preferred_employees(request, project)
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name="project",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="Specify the ID of the team to filter employees",
            required=True,
        ),
        openapi.Parameter(
            name="duration",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Specify the amount of time to add (in days or months).",
            required=True,
        ),
        openapi.Parameter(
            name="unit",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Specify the unit of time for duration (days or months).",
            required=True,
        ),
    ],
    responses={
        200: openapi.Response("Filtered Employees retrieved successfully", EmployeesSerializer(many=True)),
        400: "Invalid parameter value or team not found",
    },
)
@api_view(['GET'])
def get_preferred_team(request, project):
    try:
        employees = filter_preferred_employees(request, project)  # Use the same filtering function
        team = Teams.objects.get(project=project)

        required_skills = [skill.strip().strip('"') for skill in team.required_skills.split(',')]
        qualified_employees = calculate_best_team(employees, required_skills)  # Call your calculation logic
        if qualified_employees:  # Check if the list is not empty
            latest_availability = max(employee.availability for employee in qualified_employees)
        else:
            latest_availability = None

        serializer = EmployeesSerializer(qualified_employees, many=True)
        return Response({
            'employees': serializer.data,
            'latest_availability': latest_availability  # This will be a date or None
        }, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter(
            name="project",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description="Specify the ID of the team to filter employees",
            required=True,
        ),
    ],
    responses={
        200: openapi.Response("Filtered Employees retrieved successfully", EmployeesSerializer(many=True)),
        400: "Invalid parameter value or team not found",
    },
)
@api_view(['POST'])
def ask_chatgpt(request, project):


    employees = filter_actual_employees(project)


    employees_data = EmployeesSerializer(employees, many=True).data
    team = Teams.objects.get(project=project)

    required_skills = [skill.strip().strip('"') for skill in team.required_skills.split(',')]


    employees_list = "\n".join([
        f"Name: {e['name']}, Skills: {e['skills']}, Experience: {e['experience']} years, Availability: {e['availability']}"
        for e in employees_data
    ])
    question = (
        f"Here are the employees:\n{employees_list}\n"
        f"Required skills: {required_skills}\n"
        "Please suggest the best team based on this information with detailed explanation."
    )

    # Send the question to OpenAI using the new chat-based API format
    try:
        openai.api_key = ""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or whichever model you're using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return Response({"answer": answer}, status=status.HTTP_200_OK)
    except openai.error.OpenAIError as e:  # Ensure to handle specific OpenAI errors
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)