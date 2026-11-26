
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user, doctor, patient, Speciality

admin.site.register(user, UserAdmin)


@admin.register(doctor)
class DoctorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations médecin', {
            'fields': ('phone', 'licence_number', 'specialities')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations médecin', {
            'fields': ('phone', 'licence_number', 'specialities')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('licence_number',)
        return ()


@admin.register(patient)
class PatientAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations patient', {
            'fields': ('phone', 'birth_date', 'national_id')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations patient', {
            'fields': ('phone', 'birth_date', 'national_id')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('national_id',)
        return ()


admin.site.register(Speciality)
