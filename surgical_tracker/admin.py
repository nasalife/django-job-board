from django.contrib import admin
from .models import UserProfile, Patient, Surgeon, Surgery, MedicalEquipment, SurgeryEquipment, Activity


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'department', 'created_at']
    list_filter = ['role', 'department', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    raw_id_fields = ['user']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_birth', 'gender', 'blood_group', 'phone']
    list_filter = ['gender', 'blood_group', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    date_hierarchy = 'created_at'


@admin.register(Surgeon)
class SurgeonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialty', 'license_number', 'phone', 'email', 'years_of_experience']
    list_filter = ['specialty', 'created_at']
    search_fields = ['first_name', 'last_name', 'specialty', 'license_number', 'email']


@admin.register(Surgery)
class SurgeryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'surgeon', 'procedure_type', 'scheduled_date', 'status', 'urgency', 'operating_room']
    list_filter = ['status', 'urgency', 'scheduled_date', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'surgeon__first_name',
                    'surgeon__last_name', 'procedure_type', 'operating_room']
    date_hierarchy = 'scheduled_date'
    raw_id_fields = ['patient', 'surgeon']


@admin.register(MedicalEquipment)
class MedicalEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity_available', 'is_available', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name', 'description']


@admin.register(SurgeryEquipment)
class SurgeryEquipmentAdmin(admin.ModelAdmin):
    list_display = ['surgery', 'equipment', 'quantity_used']
    list_filter = ['equipment']
    raw_id_fields = ['surgery', 'equipment']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'related_surgery', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
