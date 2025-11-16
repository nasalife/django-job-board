from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Surgeon, Surgery, UserProfile, Activity


class PatientForm(forms.ModelForm):
    """Formulaire pour créer et modifier un patient"""

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'blood_group', 'phone', 'email', 'address',
            'medical_history', 'allergies'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse complète'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Antécédents médicaux'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Allergies connues'}),
        }


class SurgeonForm(forms.ModelForm):
    """Formulaire pour créer et modifier un chirurgien"""

    class Meta:
        model = Surgeon
        fields = [
            'first_name', 'last_name', 'specialty', 'license_number',
            'phone', 'email', 'years_of_experience'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spécialité'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de licence'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Années d'expérience"}),
        }


class SurgeryForm(forms.ModelForm):
    """Formulaire pour créer et modifier un programme chirurgical"""

    class Meta:
        model = Surgery
        fields = [
            'patient', 'surgeon', 'procedure_type', 'description',
            'scheduled_date', 'estimated_duration', 'operating_room',
            'status', 'urgency', 'anesthesia_type', 'pre_operative_notes'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'surgeon': forms.Select(attrs={'class': 'form-control'}),
            'procedure_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Type d'intervention"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Durée en minutes'}),
            'operating_room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salle'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'anesthesia_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Type d'anesthésie"}),
            'pre_operative_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription avec profil"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data.get('phone', ''),
                department=self.cleaned_data.get('department', '')
            )
        return user
