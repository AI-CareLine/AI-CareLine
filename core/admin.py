from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Hospital, Doctor, Appointment, DoctorAvailability, HospitalAdmin

class HospitalAdminFilter(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            hospital_admin = HospitalAdmin.objects.get(user=request.user)
            return qs.filter(id=hospital_admin.hospital.id)
        except HospitalAdmin.DoesNotExist:
            return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.id == hospital_admin.hospital.id
            except HospitalAdmin.DoesNotExist:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

class DoctorAdminFilter(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            hospital_admin = HospitalAdmin.objects.get(user=request.user)
            return qs.filter(hospital=hospital_admin.hospital)
        except HospitalAdmin.DoesNotExist:
            return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return True  # Shifoxona admini shifokor qo‘shishi mumkin

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.hospital == hospital_admin.hospital
            except HospitalAdmin.DoesNotExist:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.hospital == hospital_admin.hospital
            except HospitalAdmin.DoesNotExist:
                return False
        return True

class AppointmentAdminFilter(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            hospital_admin = HospitalAdmin.objects.get(user=request.user)
            return qs.filter(hospital=hospital_admin.hospital)
        except HospitalAdmin.DoesNotExist:
            return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.hospital == hospital_admin.hospital
            except HospitalAdmin.DoesNotExist:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.hospital == hospital_admin.hospital
            except HospitalAdmin.DoesNotExist:
                return False
        return True

class DoctorAvailabilityAdminFilter(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            hospital_admin = HospitalAdmin.objects.get(user=request.user)
            return qs.filter(doctor__hospital=hospital_admin.hospital)
        except HospitalAdmin.DoesNotExist:
            return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return True  # Shifoxona admini vaqt qo‘shishi mumkin

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.doctor.hospital == hospital_admin.hospital
            except HospitalAdmin.DoesNotExist:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not request.user.is_superuser:
            try:
                hospital_admin = HospitalAdmin.objects.get(user=request.user)
                return obj.doctor.hospital == hospital_admin.hospital
            except HospitalAdmin.DoesNotExist:
                return False
        return True

from django.contrib import admin
from .models import Hospital, Doctor, Appointment, DoctorAvailability, HospitalAdmin, UserProfile, Medication

# Oldingi admin filterlar (HospitalAdminFilter, DoctorAdminFilter va hokazo) shu yerda qoladi

admin.site.register(Hospital, HospitalAdminFilter)
admin.site.register(Doctor, DoctorAdminFilter)
admin.site.register(Appointment, AppointmentAdminFilter)
admin.site.register(DoctorAvailability, DoctorAvailabilityAdminFilter)
admin.site.register(HospitalAdmin)
admin.site.register(UserProfile)
admin.site.register(Medication)  # Yangi modelni qo'shamiz