from django.db import models

# Create your models here.
class Employees(models.Model):
    TEMPERAMENT_CHOICES = [
        ("melancholic", "Melancholic"),
        ("choleric", "Choleric"),
        ("sanguine", "Sanguine"),
        ("phlegmatic", "Phlegmatic"),
    ]
    name = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(unique=True)
    skills = models.TextField(help_text="List of skills, separated by commas.")
    experience = models.PositiveIntegerField(help_text="Years of experience")
    location = models.CharField(max_length=100)
    type_of_work = models.BooleanField(default=False, help_text="Indicates if the employee is able to work on projects on ethical grounds.")
    availability = models.DateField(help_text="Date the candidate is available to start")
    security_clearance = models.BooleanField(default=False, help_text="Indicates if the employee has gone through clearance process")
    temperament = models.CharField(max_length=50, choices=TEMPERAMENT_CHOICES,
                                   help_text="Select the candidate's temperament")

    def __str__(self):
        return f"{self.name} ({self.email})"


    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'