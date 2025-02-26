from .views import  employees_list_view, filtered_employees_list_view,ask_chatgpt, create_employee, get_preferred_team, get_ideal_team, get_actual_team
from django.urls import path

urlpatterns = [

    path('', employees_list_view, name='employees-list'),
    path('filetered-employees/', filtered_employees_list_view, name='filtered-employees-list'),
    path('create_employee/', create_employee, name='create_employee'),
    path('ideal_team/<str:project>/',  get_ideal_team, name='get_ideal_team'),
    path('actual_team/<str:project>/',  get_actual_team, name='get_actual_team'),
    path('get_preferred_team/<str:project>/',  get_preferred_team, name='get_preferred_team'),
    path('ask/<str:project>/', ask_chatgpt, name='ask_chatgpt'),
]