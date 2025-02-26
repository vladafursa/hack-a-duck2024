from django.db import models

class Teams(models.Model):
    project = models.CharField(max_length=100, primary_key=True)
    required_skills = models.TextField(help_text="List of required, separated by commas.")
    location = models.CharField(max_length=100)
    type_of_work = models.BooleanField(default=False, help_text="Indicates if the employee is able to work on projects on ethical grounds.")
    start_date = models.DateField(help_text="date when the project starts")
    security_clearance = models.BooleanField(default=False, help_text="Indicates if the employee has gone through clearance process")
    team_size = models.IntegerField(max_length=50)
    experience = models.PositiveIntegerField(help_text="Years of experience", default=0)

    def __str__(self):
        return self.project


    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'