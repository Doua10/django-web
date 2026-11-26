
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Status(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmé'
    CANCELLED = 'CANCELLED', 'Annulé'


class Appointment(models.Model):

    reason = models.TextField()

    duration_minutes = models.PositiveIntegerField(default=30)

    appointment_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    doctor = models.ForeignKey(
        'AccountApp.doctor',
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        'AccountApp.patient',
        on_delete=models.CASCADE
    )

    def clean(self):
        super().clean()

        if self.appointment_date:
            date_changed = True

            if self.pk:
                old_appointment = Appointment.objects.filter(
                    pk=self.pk
                ).first()

                if old_appointment:
                    date_changed = (
                        old_appointment.appointment_date
                        != self.appointment_date
                    )

            if date_changed and self.appointment_date <= timezone.now():
                raise ValidationError({
                    'appointment_date':
                    "La date du rendez-vous doit être dans le futur."
                })

    class Meta:
        ordering = ['appointment_date']

        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment'
            )
        ]
