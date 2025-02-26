from .views import teams_list_view, create_team, chosen_team, advice
from django.urls import path

urlpatterns = [
    path('', teams_list_view, name='teams-list'),
    path('create-team/', create_team, name='create_team'),
    path('team/<str:project>/', chosen_team, name='chosen_team'),
]