from django.db import models
from django.utils import timezone


class Patient(models.Model):
    """Modèle pour les patients"""
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sexe")
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, verbose_name="Groupe sanguin")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(verbose_name="Adresse")
    medical_history = models.TextField(blank=True, null=True, verbose_name="Antécédents médicaux")
    allergies = models.TextField(blank=True, null=True, verbose_name="Allergies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class Surgeon(models.Model):
    """Modèle pour les chirurgiens"""
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    specialty = models.CharField(max_length=200, verbose_name="Spécialité")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de licence")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    years_of_experience = models.IntegerField(default=0, verbose_name="Années d'expérience")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chirurgien"
        verbose_name_plural = "Chirurgiens"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialty}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Surgery(models.Model):
    """Modèle pour les programmes chirurgicaux"""
    STATUS_CHOICES = [
        ('pending', 'En Attente'),
        ('scheduled', 'Planifié'),
        ('in_progress', 'En Cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]

    URGENCY_CHOICES = [
        ('elective', 'Programmée'),
        ('urgent', 'Urgente'),
        ('emergency', 'Urgence vitale'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='surgeries', verbose_name="Patient")
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE, related_name='surgeries', verbose_name="Chirurgien")
    procedure_type = models.CharField(max_length=200, verbose_name="Type d'intervention")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    scheduled_date = models.DateTimeField(verbose_name="Date prévue")
    actual_start_time = models.DateTimeField(blank=True, null=True, verbose_name="Heure de début réelle")
    actual_end_time = models.DateTimeField(blank=True, null=True, verbose_name="Heure de fin réelle")
    estimated_duration = models.IntegerField(help_text="Durée estimée en minutes", verbose_name="Durée estimée (min)")
    operating_room = models.CharField(max_length=50, verbose_name="Salle d'opération")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='elective', verbose_name="Urgence")
    pre_operative_notes = models.TextField(blank=True, null=True, verbose_name="Notes pré-opératoires")
    post_operative_notes = models.TextField(blank=True, null=True, verbose_name="Notes post-opératoires")
    complications = models.TextField(blank=True, null=True, verbose_name="Complications")
    anesthesia_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type d'anesthésie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Programme Chirurgical"
        verbose_name_plural = "Programmes Chirurgicaux"
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.procedure_type} - {self.patient.full_name} ({self.scheduled_date.strftime('%d/%m/%Y')})"

    @property
    def actual_duration(self):
        """Calcule la durée réelle de l'intervention en minutes"""
        if self.actual_start_time and self.actual_end_time:
            delta = self.actual_end_time - self.actual_start_time
            return int(delta.total_seconds() / 60)
        return None


class MedicalEquipment(models.Model):
    """Modèle pour le matériel médical"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    quantity_available = models.IntegerField(default=0, verbose_name="Quantité disponible")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Matériel Médical"
        verbose_name_plural = "Matériels Médicaux"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.quantity_available} disponible)"


class SurgeryEquipment(models.Model):
    """Modèle pour associer le matériel à une chirurgie"""
    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE, related_name='equipment', verbose_name="Chirurgie")
    equipment = models.ForeignKey(MedicalEquipment, on_delete=models.CASCADE, verbose_name="Matériel")
    quantity_used = models.IntegerField(default=1, verbose_name="Quantité utilisée")

    class Meta:
        verbose_name = "Matériel pour Chirurgie"
        verbose_name_plural = "Matériels pour Chirurgie"
        unique_together = ['surgery', 'equipment']

    def __str__(self):
        return f"{self.equipment.name} pour {self.surgery}"


class Activity(models.Model):
    """Modèle pour le journal d'activités"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    related_surgery = models.ForeignKey(Surgery, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='activities', verbose_name="Chirurgie associée")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
