from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Patient, Surgeon, Surgery, Activity


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
