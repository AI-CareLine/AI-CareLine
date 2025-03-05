from django.shortcuts import render
from .models import Hospital, Doctor, Appointment, DISTRICT_CHOICES, DOCTOR_TYPE_CHOICES, DOCTOR_SPECIALTY_CHOICES, DoctorAvailability  # DOCTOR_TYPE_CHOICES qo'shildi
from django.contrib.auth.decorators import login_required


# Bosh sahifa
def home(request):
    return render(request, 'core/home.html')

# Shifoxonalar ro‘yxati
def hospital_list(request):
    district = request.GET.get('district')  # Tuman filtri
    hospitals = Hospital.objects.all()
    if district:
        hospitals = hospitals.filter(district=district)
    context = {
        'hospitals': hospitals,
        'district_choices': DISTRICT_CHOICES,
    }
    return render(request, 'core/hospital_list.html', context)

# Shifoxona tafsilotlari
def hospital_detail(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    doctors = Doctor.objects.filter(hospital=hospital)
    context = {
        'hospital': hospital,
        'doctors': doctors,
    }
    return render(request, 'core/hospital_detail.html', context)

# Doktor turini aniqlash
def doctor_type(request):
    specialty = request.GET.get('specialty')
    district = request.GET.get('district')
    recommended_type = None
    doctors = Doctor.objects.all()

    if specialty:
        for key, _, doctor_type in DOCTOR_SPECIALTY_CHOICES:
            if key == specialty:
                recommended_type = doctor_type
                doctors = doctors.filter(doctor_type=key)
                break
    if district:
        doctors = doctors.filter(hospital__district=district)

    context = {
        'doctors': doctors,
        'specialty_choices': [(key, desc) for key, desc, _ in DOCTOR_SPECIALTY_CHOICES],
        'district_choices': DISTRICT_CHOICES,
        'recommended_type': recommended_type,
    }
    return render(request, 'core/doctor_type.html', context)

from django.shortcuts import render, redirect
from .models import Hospital, Doctor, Appointment, DISTRICT_CHOICES, DOCTOR_TYPE_CHOICES

# Boshqa view’lar (oldingi kodlar shu yerda qoladi)

# Shifoxonadagi shifokorlar ro‘yxati
def hospital_doctors(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    doctors = Doctor.objects.filter(hospital=hospital)
    context = {
        'hospital': hospital,
        'doctors': doctors,
    }
    return render(request, 'core/hospital_doctors.html', context)



# Oldingi view’lar shu yerda qoladi

# Shifokor detallari va navbat olish
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Global ma'lumotlar seti (avvalgi SYMPTOMS_DATA va DOCTOR_SPECIALTY_CHOICES shu yerda qoladi)

@login_required
def doctor_type(request):
    specialty = request.GET.get('specialty')
    district = request.GET.get('district')
    doctors = Doctor.objects.all()
    
    if specialty:
        # specialty bu yerda shifokorning to‘liq nomi (masalan, "Stomatolog")
        # DOCTOR_SPECIALTY_CHOICES dan mos key (masalan, "stomatolog") ni topamiz
        doctor_type_key = None
        for key, _, name in DOCTOR_SPECIALTY_CHOICES:
            if name.lower() == specialty.lower():
                doctor_type_key = key
                break
        if doctor_type_key:
            doctors = doctors.filter(doctor_type=doctor_type_key)
    
    if district:
        doctors = doctors.filter(hospital__district=district)

    context = {
        'doctors': doctors,
        'specialty_choices': [(key, desc) for key, desc, _ in DOCTOR_SPECIALTY_CHOICES],
        'district_choices': DISTRICT_CHOICES,
        'recommended_type': specialty,  # Tavsiya etilgan shifokor turini kontekstga qo'shamiz
    }
    return render(request, 'core/doctor_type.html', context)

# Qolgan view’lar (consultant, hospital_list va hokazo) shu yerda qoladi
@login_required
def appointment(request):
    district = request.GET.get('district')
    hospital_id = request.GET.get('hospital')
    doctor_id = request.GET.get('doctor')

    hospitals = Hospital.objects.all()
    if district:
        hospitals = hospitals.filter(district=district)
    
    doctors = Doctor.objects.all()
    if hospital_id:
        doctors = doctors.filter(hospital__id=hospital_id)
    
    available_times = None
    selected_doctor = None
    if doctor_id:
        selected_doctor = Doctor.objects.get(id=doctor_id)
        available_times = DoctorAvailability.objects.filter(doctor=selected_doctor, is_available=True)

    if request.method == 'POST':
        patient_name = request.user.username
        availability_id = request.POST.get('availability')
        availability = DoctorAvailability.objects.get(id=availability_id)
        appointment = Appointment(
            hospital=availability.doctor.hospital,
            doctor=availability.doctor,
            user=request.user,
            patient_name=patient_name,
            start_time=availability.start_time,
            end_time=availability.end_time,
            is_booked=True
        )
        appointment.save()
        availability.is_available = False
        availability.save()
        return render(request, 'core/appointment_success.html', {'appointment': appointment})

    context = {
        'hospitals': hospitals,
        'doctors': doctors,
        'district_choices': DISTRICT_CHOICES,
        'selected_doctor': selected_doctor,
        'available_times': available_times,
    }
    return render(request, 'core/appointment.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})






from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Global ma'lumotlar seti
SYMPTOMS_DATA = {
    'umumiy': ['charchoq', 'issiq', 'bosh og‘rig‘i', 'nafas qisilishi'],
    'pediatr': ['tovush chiqarish qiyinligi', 'issiq', 'ovqat hazm qilish muammosi', 'ko‘z yoshi'],
    'kardiolog': ['ko‘krak og‘rig‘i', 'nafas qisilishi', 'yurak urishi tezligi', 'bosh aylanishi'],
    'dermatolog': ['teri qizarishi', 'teri qichishi', 'teri bo‘shlig‘i', 'tish sargayishi'],
    'nevrolog': ['bosh og‘rig‘i', 'qo‘l titrashi', 'uyqu muammosi', 'xotira zaifligi'],
    'oftalmolog': ['ko‘z xiralashuvi', 'ko‘z og‘rig‘i', 'ko‘z yoshi', 'ko‘rinish xira'],
    'lor': ['tomog‘ og‘rig‘i', 'burun tiqilishi', 'quloq og‘rig‘i', 'ovoz xiralashuvi'],
    'radiolog': ['og‘riq lokalizatsiyasi', 'tashxis qilish uchun tasvir', 'noma’lum alomatlar'],
    'ortoped': ['suyak og‘rig‘i', 'bo‘g‘im shishishi', 'mushak kuchsizligi', 'og‘riq harakatsiz holatda'],
    'stomatolog': ['tish og‘rig‘i', 'tish sargayishi', 'og‘iz og‘rig‘i', 'tish to‘qimalarining buzilishi'],
    'ichki_kasalliklar': ['ichak og‘rig‘i', 'ovqat hazm qilish muammosi', 'qorin shishi', 'nafas qisilishi'],
    'urolog': ['siydik yo‘li og‘rig‘i', 'siydik chiqarish qiyinligi', 'qon siydikda', 'ichak og‘rig‘i'],
    'ginekolog': ['ayol organlari og‘rig‘i', 'ovqat hazm qilish muammosi', 'qon ketishi', 'qorin shishi'],
    'onkolog': ['og‘riq lokalizatsiyasi', 'vazn yo‘qotish', 'charchoq', 'terida o‘zgarish'],
    'shoshilinch': ['katta og‘riq', 'nafas qisilishi', 'bosh aylanishi', 'ko‘krak og‘rig‘i'],
    'yuqumli': ['issiq', 'tog‘iz qichishi', 'tushishi', 'ko‘z yoshi'],
    'fizioterapevt': ['mushak og‘rig‘i', 'bo‘g‘im shishishi', 'harakat qiyinligi', 'kuchsizlik'],
    'dietolog': ['vazn oshirish', 'vazn yo‘qotish', 'ovqat hazm qilish muammosi', 'charchoq'],
    'psixolog': ['uyqu muammosi', 'stress', 'tashvish', 'depressiya'],
}
from .models import UserProfile

@login_required
def consultant(request):
    recommended_doctor = None
    symptoms = request.GET.getlist('symptoms', [])
    search_query = request.GET.get('search', '')
    suggestions = []

    if search_query:
        for doctor_type, symptoms_list in SYMPTOMS_DATA.items():
            for symptom in symptoms_list:
                if search_query.lower() in symptom.lower():
                    if symptom not in suggestions:
                        suggestions.append(symptom)

    if symptoms:
        doctor_scores = {}
        for doctor_type, symptoms_list in SYMPTOMS_DATA.items():
            score = len(set(symptoms) & set(symptoms_list))
            if score > 0:
                doctor_scores[doctor_type] = score

        if doctor_scores:
            recommended_doctor = max(doctor_scores.items(), key=lambda x: x[1])[0]
            for key, _, name in DOCTOR_SPECIALTY_CHOICES:
                if key == recommended_doctor:
                    recommended_doctor = name
                    break
            # Tavsiya etilgan shifokorni foydalanuvchi profiliga saqlash
            user_profile = request.user.userprofile
            user_profile.recommended_doctor = recommended_doctor
            user_profile.save()

    context = {
        'recommended_doctor': recommended_doctor,
        'symptoms': symptoms,
        'suggestions': suggestions,
        'symptoms_data': SYMPTOMS_DATA,
    }
    return render(request, 'core/consultant.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Hospital, Doctor, Appointment, DoctorAvailability, DISTRICT_CHOICES, DOCTOR_SPECIALTY_CHOICES

# Boshqa view’lar (home, hospital_list, hospital_detail, hospital_doctors, consultant, doctor_type, appointment) shu yerda

@login_required
def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    available_times = DoctorAvailability.objects.filter(doctor=doctor, is_available=True)
    
    if request.method == 'POST':
        patient_name = request.user.username
        availability_id = request.POST.get('availability')
        availability = DoctorAvailability.objects.get(id=availability_id)
        appointment = Appointment(
            hospital=doctor.hospital,
            doctor=doctor,
            user=request.user,  # Foydalanuvchini saqlash
            patient_name=patient_name,
            start_time=availability.start_time,
            end_time=availability.end_time,
            is_booked=True
        )
        appointment.save()
        availability.is_available = False
        availability.save()
        return render(request, 'core/appointment_success.html', {'appointment': appointment})
    
    context = {
        'doctor': doctor,
        'available_times': available_times,
    }
    return render(request, 'core/doctor_detail.html', context)





from .models import UserProfile, Medication
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Medication, Appointment

@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    medications = Medication.objects.filter(user_profile=user_profile)
    appointments = Appointment.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'first_name' in request.POST:
            user_profile.first_name = request.POST.get('first_name', '')
            user_profile.last_name = request.POST.get('last_name', '')
            user_profile.phone_number = request.POST.get('phone_number', '')
            user_profile.email = request.POST.get('email', '')
            user_profile.save()
            return JsonResponse({'success': True})
        elif 'medication_name' in request.POST:
            medication = Medication(
                user_profile=user_profile,
                name=request.POST.get('medication_name', ''),
                timing=request.POST.get('timing', ''),
                start_date=request.POST.get('start_date', ''),
                end_date=request.POST.get('end_date', ''),
                instructions=request.POST.get('instructions', '')
            )
            medication.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    context = {
        'user_profile': user_profile,
        'medications': medications,
        'appointments': appointments,
    }
    return render(request, 'core/profile.html', context)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DoctorAvailability

@csrf_exempt
def check_availability(request):
    if request.method == 'POST':
        availability_id = request.POST.get('availability_id')
        try:
            availability = DoctorAvailability.objects.get(id=availability_id)
            return JsonResponse({'is_available': availability.is_available})
        except DoctorAvailability.DoesNotExist:
            return JsonResponse({'is_available': False})
    return JsonResponse({'is_available': False})