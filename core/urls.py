from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospital/<int:hospital_id>/', views.hospital_detail, name='hospital_detail'),
    path('hospital/<int:hospital_id>/doctors/', views.hospital_doctors, name='hospital_doctors'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor-type/', views.doctor_type, name='doctor_type'),
    path('appointment/', views.appointment, name='appointment'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('consultant/', views.consultant, name='consultant'),
    path('profile/', views.profile, name='profile'),
    path('check-availability/', views.check_availability, name='check_availability'),  # Yangi endpoint
]