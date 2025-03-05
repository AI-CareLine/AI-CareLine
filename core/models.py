from django.db import models

# Tumanlar uchun tanlov ro‘yxati
DISTRICT_CHOICES = (
    ('bektemir', 'Bektemir tumani'),
    ('chilonzor', 'Chilonzor tumani'),
    ('mirzo_ulugbek', 'Mirzo Ulugbek tumani'),
    ('mirobod', 'Mirobod tumani'),
    ('sergeli', 'Sergeli tumani'),
    ('shayxontohur', 'Shayxontohur tumani'),
    ('olmazor', 'Olmazor tumani'),
    ('uchtepa', 'Uchtepa tumani'),
    ('yakkasaroy', 'Yakkasaroy tumani'),
    ('yashnobod', 'Yashnobod tumani'),
    ('yunusobod', 'Yunusobod tumani'),
)

# Shifokor turlari uchun tanlov ro‘yxati
# Doktor tavsiya uchun yangi ro‘yxat
DOCTOR_SPECIALTY_CHOICES = (
    ('umumiy', 'Birlamchi tibbiy yordam ko‘rsatadigan shifokorlar', 'Umumiy shifokor'),
    ('pediatr', 'Chaqaloqlar, bolalar va yoshlar sog‘lig‘i bilan shug‘ullanadigan shifokorlar', 'Pediatr'),
    ('kardiolog', 'Yurak va qon aylanish tizimi kasalliklari bilan shug‘ullanadigan shifokorlar', 'Kardiolog'),
    ('dermatolog', 'Teri, tirnoq va soch kasalliklari bilan shug‘ullanadigan shifokorlar', 'Dermatolog'),
    ('nevrolog', 'Miya va asab tizimi kasalliklari bilan shug‘ullanadigan shifokorlar', 'Nevrolog'),
    ('oftalmolog', 'Ko‘z kasalliklari bilan shug‘ullanadigan shifokorlar', 'Oftalmolog'),
    ('lor', 'Quloq, burun va tomoq kasalliklari bilan shug‘ullanadigan shifokorlar', 'LOR'),
    ('radiolog', 'Radiatsiya texnologiyalari bilan diagnostika qiluvchi shifokorlar', 'Radiolog'),
    ('ortoped', 'Suyak, bo‘g‘im va mushak tizimi kasalliklari bilan shug‘ullanadigan shifokorlar', 'Ortoped'),
    ('stomatolog', 'Og‘iz va tish salomatligi bilan shug‘ullanadigan shifokorlar', 'Stomatolog'),
    ('ichki_kasalliklar', 'Kattalardagi tibbiy muammolarni davolaydigan shifokorlar', 'Ichki kasalliklar bo‘yicha mutaxassis'),
    ('urolog', 'Siydik yo‘llari va jinsiy a‘zolar bilan bog‘liq muammolar bilan shug‘ullanadigan shifokorlar', 'Urolog'),
    ('ginekolog', 'Ayollar reproduktiv organlari bilan shug‘ullanadigan shifokorlar', 'Ginekolog'),
    ('onkolog', 'Saraton kasalliklari bilan shug‘ullanadigan shifokorlar', 'Onkolog'),
    ('shoshilinch', 'Favqulodda vaziyatlarda shug‘ullanadigan shifokorlar', 'Shoshilinch tibbiy yordam shifokori'),
    ('yuqumli', 'Yuqumli kasalliklar bilan shug‘ullanadigan shifokorlar', 'Yuqumli kasalliklar bo‘yicha mutaxassis'),
    ('fizioterapevt', 'Jismoniy mashqlar bilan davolovchi mutaxassislar', 'Fizioterapevt'),
    ('dietolog', 'Oziqlanish va parhezga ixtisoslashgan mutaxassislar', 'Dietolog'),
    ('psixolog', 'Ruhiy salomatlik muammolari bilan shug‘ullanadigan mutaxassislar', 'Psixolog'),
)

# Eski DOCTOR_TYPE_CHOICES o‘rnini ushbu yangi format bilan almashtirish uchun
DOCTOR_TYPE_CHOICES = [(key, name) for key, _, name in DOCTOR_SPECIALTY_CHOICES]

# Shifoxona modeli
class Hospital(models.Model):
    name = models.CharField(max_length=255, verbose_name="Shifoxona nomi")
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)

    image = models.ImageField(upload_to='hospital_images/', null=True, blank=True, verbose_name="Shifoxona rasmi")
    rating = models.FloatField(default=0.0, verbose_name="Reyting")
    phone_number = models.CharField(max_length=15, verbose_name="Shifoxona raqami")
    emergency_number = models.CharField(max_length=15, verbose_name="Tez yordam raqami")
    working_hours = models.CharField(max_length=100, verbose_name="Ishlash vaqtlari")

    def __str__(self):
        return self.name

# Shifokor modeli
class Doctor(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name="Shifoxona")
    image = models.ImageField(upload_to='doctor_images/', null=True, blank=True, verbose_name="Shifokor rasmi")
    doctor_type = models.CharField(max_length=50, choices=DOCTOR_TYPE_CHOICES, verbose_name="Shifokor turi")
    first_name = models.CharField(max_length=100, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, verbose_name="Familyasi")
    experience_years = models.IntegerField(verbose_name="Tajriba (yil)")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qabul narxi")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_doctor_type_display()}"

# Navbat modeli
from django.contrib.auth.models import User

class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name="Shifoxona")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Shifokor")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")  # Yangi maydon
    patient_name = models.CharField(max_length=100, verbose_name="Bemor ismi")
    start_time = models.DateTimeField(verbose_name="Boshlanish vaqti")
    end_time = models.DateTimeField(verbose_name="Tugash vaqti")
    is_booked = models.BooleanField(default=True, verbose_name="Band qilinganmi")

    def __str__(self):
        return f"{self.patient_name} - {self.doctor} ({self.start_time})"
    

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Shifokor")
    start_time = models.DateTimeField(verbose_name="Boshlanish vaqti")
    end_time = models.DateTimeField(verbose_name="Tugash vaqti")
    is_available = models.BooleanField(default=True, verbose_name="Bo‘shmi")

    def __str__(self):
        return f"{self.doctor} - {self.start_time} to {self.end_time}"
    

from django.contrib.auth.models import User

class HospitalAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name="Shifoxona")

    def __str__(self):
        return f"{self.user.username} - {self.hospital.name}"
    





from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
import json


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Familyasi")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Telefon raqami")
    email = models.EmailField(blank=True, verbose_name="Email")
    recommended_doctor = models.CharField(max_length=50, blank=True, verbose_name="Tavsiya etilgan shifokor")

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"
    


class Medication(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Foydalanuvchi profili")
    name = models.CharField(max_length=100, verbose_name="Dori nomi")
    timing = models.CharField(max_length=100, verbose_name="Ichish vaqti (masalan, abedda ertalab)")  # Masalan, "nonushtadan oldin", "kechqurun"
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi")
    instructions = models.TextField(blank=True, verbose_name="Qo‘shimcha ko‘rsatmalar")

    def __str__(self):
        return f"{self.name} - {self.user_profile.user.username}"