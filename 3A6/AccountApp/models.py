
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )


class user(AbstractUser):
    pass


class doctor(user):
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    licence_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )

    specialities = models.ManyToManyField(
        'Speciality',
        related_name='doctors',
        blank=True
    )

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


class patient(user):
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    birth_date = models.DateField(
        validators=[validate_past_date]
    )

    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Speciality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'
