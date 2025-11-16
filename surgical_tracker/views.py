from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Patient, Surgeon, Surgery, Activity, UserProfile
from .forms import PatientForm, SurgeonForm, SurgeryForm, UserRegistrationForm


def dashboard(request):
    """Vue principale du dashboard"""
    # Statistiques des chirurgies
    total_surgeries = Surgery.objects.count()
    completed_surgeries = Surgery.objects.filter(status='completed').count()
    pending_surgeries = Surgery.objects.filter(status__in=['pending', 'scheduled']).count()
    cancelled_surgeries = Surgery.objects.filter(status='cancelled').count()

    # Prochains programmes (7 prochains jours)
    today = timezone.now()
    next_week = today + timedelta(days=7)
    upcoming_surgeries = Surgery.objects.filter(
        scheduled_date__gte=today,
        scheduled_date__lte=next_week,
        status__in=['pending', 'scheduled']
    ).select_related('patient', 'surgeon')[:5]

    # Activités récentes
    recent_activities = Activity.objects.all()[:5]

    # Derniers programmes chirurgicaux
    recent_surgeries = Surgery.objects.select_related('patient', 'surgeon').all()[:10]

    context = {
        'total_surgeries': total_surgeries,
        'completed_surgeries': completed_surgeries,
        'pending_surgeries': pending_surgeries,
        'cancelled_surgeries': cancelled_surgeries,
        'upcoming_surgeries': upcoming_surgeries,
        'recent_activities': recent_activities,
        'recent_surgeries': recent_surgeries,
        'current_year': datetime.now().year,
    }

    return render(request, 'surgical_tracker/dashboard.html', context)


def surgery_list(request):
    """Liste des programmes chirurgicaux"""
    surgeries = Surgery.objects.select_related('patient', 'surgeon').all()

    context = {
        'surgeries': surgeries,
        'current_year': datetime.now().year,
    }

    return render(request, 'surgical_tracker/surgery_list.html', context)


def patient_list(request):
    """Liste des patients"""
    patients = Patient.objects.all()

    context = {
        'patients': patients,
        'current_year': datetime.now().year,
    }

    return render(request, 'surgical_tracker/patient_list.html', context)


def surgeon_list(request):
    """Liste des chirurgiens"""
    surgeons = Surgeon.objects.all()

    context = {
        'surgeons': surgeons,
        'current_year': datetime.now().year,
    }

    return render(request, 'surgical_tracker/surgeon_list.html', context)


def calendar_view(request):
    """Vue du calendrier des interventions"""
    context = {
        'current_year': datetime.now().year,
    }

    return render(request, 'surgical_tracker/calendar.html', context)


# ===== VUES D'AUTHENTIFICATION =====

def user_login(request):
    """Vue de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.get_full_name() or user.username}!')

            # Redirection selon le rôle
            if hasattr(user, 'profile'):
                if user.profile.is_secretary:
                    return redirect('surgical_tracker:secretary_dashboard')
            return redirect('surgical_tracker:dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'surgical_tracker/login.html', {'current_year': datetime.now().year})


@login_required
def user_logout(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('surgical_tracker:login')


def user_register(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('surgical_tracker:login')
    else:
        form = UserRegistrationForm()

    return render(request, 'surgical_tracker/register.html', {
        'form': form,
        'current_year': datetime.now().year
    })


# ===== VUES CRUD PATIENT =====

@login_required
def patient_create(request):
    """Créer un nouveau patient"""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.full_name} ajouté avec succès!')
            return redirect('surgical_tracker:patient_list')
    else:
        form = PatientForm()

    return render(request, 'surgical_tracker/patient_form.html', {
        'form': form,
        'title': 'Nouveau Patient',
        'current_year': datetime.now().year
    })


@login_required
def patient_update(request, pk):
    """Modifier un patient"""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.full_name} modifié avec succès!')
            return redirect('surgical_tracker:patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'surgical_tracker/patient_form.html', {
        'form': form,
        'patient': patient,
        'title': f'Modifier {patient.full_name}',
        'current_year': datetime.now().year
    })


@login_required
def patient_delete(request, pk):
    """Supprimer un patient"""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        name = patient.full_name
        patient.delete()
        messages.success(request, f'Patient {name} supprimé avec succès!')
        return redirect('surgical_tracker:patient_list')

    return render(request, 'surgical_tracker/patient_confirm_delete.html', {
        'patient': patient,
        'current_year': datetime.now().year
    })


@login_required
def patient_detail(request, pk):
    """Détail d'un patient"""
    patient = get_object_or_404(Patient, pk=pk)
    surgeries = patient.surgeries.all().order_by('-scheduled_date')

    return render(request, 'surgical_tracker/patient_detail.html', {
        'patient': patient,
        'surgeries': surgeries,
        'current_year': datetime.now().year
    })


# ===== VUES CRUD SURGEON =====

@login_required
def surgeon_create(request):
    """Créer un nouveau chirurgien"""
    if request.method == 'POST':
        form = SurgeonForm(request.POST)
        if form.is_valid():
            surgeon = form.save()
            messages.success(request, f'Chirurgien Dr. {surgeon.full_name} ajouté avec succès!')
            return redirect('surgical_tracker:surgeon_list')
    else:
        form = SurgeonForm()

    return render(request, 'surgical_tracker/surgeon_form.html', {
        'form': form,
        'title': 'Nouveau Chirurgien',
        'current_year': datetime.now().year
    })


@login_required
def surgeon_update(request, pk):
    """Modifier un chirurgien"""
    surgeon = get_object_or_404(Surgeon, pk=pk)

    if request.method == 'POST':
        form = SurgeonForm(request.POST, instance=surgeon)
        if form.is_valid():
            surgeon = form.save()
            messages.success(request, f'Chirurgien Dr. {surgeon.full_name} modifié avec succès!')
            return redirect('surgical_tracker:surgeon_list')
    else:
        form = SurgeonForm(instance=surgeon)

    return render(request, 'surgical_tracker/surgeon_form.html', {
        'form': form,
        'surgeon': surgeon,
        'title': f'Modifier Dr. {surgeon.full_name}',
        'current_year': datetime.now().year
    })


@login_required
def surgeon_delete(request, pk):
    """Supprimer un chirurgien"""
    surgeon = get_object_or_404(Surgeon, pk=pk)

    if request.method == 'POST':
        name = surgeon.full_name
        surgeon.delete()
        messages.success(request, f'Chirurgien Dr. {name} supprimé avec succès!')
        return redirect('surgical_tracker:surgeon_list')

    return render(request, 'surgical_tracker/surgeon_confirm_delete.html', {
        'surgeon': surgeon,
        'current_year': datetime.now().year
    })


@login_required
def surgeon_detail(request, pk):
    """Détail d'un chirurgien"""
    surgeon = get_object_or_404(Surgeon, pk=pk)
    surgeries = surgeon.surgeries.all().order_by('-scheduled_date')

    return render(request, 'surgical_tracker/surgeon_detail.html', {
        'surgeon': surgeon,
        'surgeries': surgeries,
        'current_year': datetime.now().year
    })


# ===== VUES CRUD SURGERY =====

@login_required
def surgery_create(request):
    """Créer un nouveau programme chirurgical"""
    if request.method == 'POST':
        form = SurgeryForm(request.POST)
        if form.is_valid():
            surgery = form.save()
            messages.success(request, f'Programme chirurgical créé avec succès!')
            return redirect('surgical_tracker:surgery_list')
    else:
        form = SurgeryForm()

    return render(request, 'surgical_tracker/surgery_form.html', {
        'form': form,
        'title': 'Nouveau Programme Chirurgical',
        'current_year': datetime.now().year
    })


@login_required
def surgery_update(request, pk):
    """Modifier un programme chirurgical"""
    surgery = get_object_or_404(Surgery, pk=pk)

    if request.method == 'POST':
        form = SurgeryForm(request.POST, instance=surgery)
        if form.is_valid():
            surgery = form.save()
            messages.success(request, f'Programme chirurgical modifié avec succès!')
            return redirect('surgical_tracker:surgery_list')
    else:
        form = SurgeryForm(instance=surgery)

    return render(request, 'surgical_tracker/surgery_form.html', {
        'form': form,
        'surgery': surgery,
        'title': 'Modifier Programme Chirurgical',
        'current_year': datetime.now().year
    })


@login_required
def surgery_detail(request, pk):
    """Détail d'un programme chirurgical"""
    surgery = get_object_or_404(Surgery, pk=pk)

    return render(request, 'surgical_tracker/surgery_detail.html', {
        'surgery': surgery,
        'current_year': datetime.now().year
    })


# ===== INTERFACE SECRÉTAIRE =====

@login_required
def secretary_dashboard(request):
    """Dashboard spécifique pour les secrétaires"""
    # Vérifier si l'utilisateur est secrétaire
    if not hasattr(request.user, 'profile') or not request.user.profile.is_secretary:
        messages.error(request, 'Accès refusé. Cette page est réservée aux secrétaires.')
        return redirect('surgical_tracker:dashboard')

    # Statistiques
    total_patients = Patient.objects.count()
    total_surgeons = Surgeon.objects.count()
    pending_surgeries = Surgery.objects.filter(status__in=['pending', 'scheduled']).count()

    # Rendez-vous du jour
    today = timezone.now().date()
    today_surgeries = Surgery.objects.filter(
        scheduled_date__date=today
    ).select_related('patient', 'surgeon').order_by('scheduled_date')

    # Prochains rendez-vous (7 jours)
    next_week = today + timedelta(days=7)
    upcoming_surgeries = Surgery.objects.filter(
        scheduled_date__date__gt=today,
        scheduled_date__date__lte=next_week,
        status__in=['pending', 'scheduled']
    ).select_related('patient', 'surgeon').order_by('scheduled_date')[:10]

    # Patients récents
    recent_patients = Patient.objects.all().order_by('-created_at')[:5]

    context = {
        'total_patients': total_patients,
        'total_surgeons': total_surgeons,
        'pending_surgeries': pending_surgeries,
        'today_surgeries': today_surgeries,
        'upcoming_surgeries': upcoming_surgeries,
        'recent_patients': recent_patients,
        'current_year': datetime.now().year,
    }

    return render(request, 'surgical_tracker/secretary_dashboard.html', context)
