from django.urls import path
from . import views

app_name = 'surgical_tracker'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Authentification
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Chirurgiens
    path('surgeons/', views.surgeon_list, name='surgeon_list'),
    path('surgeons/create/', views.surgeon_create, name='surgeon_create'),
    path('surgeons/<int:pk>/', views.surgeon_detail, name='surgeon_detail'),
    path('surgeons/<int:pk>/update/', views.surgeon_update, name='surgeon_update'),
    path('surgeons/<int:pk>/delete/', views.surgeon_delete, name='surgeon_delete'),

    # Programmes chirurgicaux
    path('surgeries/', views.surgery_list, name='surgery_list'),
    path('surgeries/create/', views.surgery_create, name='surgery_create'),
    path('surgeries/<int:pk>/', views.surgery_detail, name='surgery_detail'),
    path('surgeries/<int:pk>/update/', views.surgery_update, name='surgery_update'),

    # Calendrier
    path('calendar/', views.calendar_view, name='calendar'),

    # Interface secrétaire
    path('secretary/', views.secretary_dashboard, name='secretary_dashboard'),
]
