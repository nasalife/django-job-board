from django.urls import path
from . import views

app_name = 'surgical_tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('surgeries/', views.surgery_list, name='surgery_list'),
    path('patients/', views.patient_list, name='patient_list'),
    path('surgeons/', views.surgeon_list, name='surgeon_list'),
    path('calendar/', views.calendar_view, name='calendar'),
]
