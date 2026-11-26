
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'doctor',
        'patient',
        'appointment_date',
        'duration_minutes',
        'status'
    )

    list_filter = ('status', 'appointment_date')
