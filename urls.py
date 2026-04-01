"""
URL configuration for homeo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from homeo.models import doctor_tbl
from . import views
from django.conf import settings
from django.conf.urls.static import static


# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path('', views.index, name='index'),

    # Authentication
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),

    # Patient
    # path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    # path('profile/', views.profile, name='profile'),

    # Admin Custom Pages
    # path('adminpage/', views.adminpage, name='adminpage'),
    # path('adminpage/add_doctor/', views.add_doctor, name='add_doctor'),
    # path('adminpage/add_medicine/', views.add_medicine, name='add_medicine'),

    # Doctor
    # path('edit_doctor/<int:id>/', views.edit_doctor, name='edit_doctor'),
    # path('delete_doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),

    # Medicine
    # path('edit_medicine/<int:id>/', views.edit_medicine, name='edit_medicine'),
    # path('delete_medicine/<int:id>/', views.delete_medicine, name='delete_medicine'),

    # Appointments
    # path('make_appointment/', views.make_appointment, name='make_appointment'),
    # path('manage_appointments/', views.manage_appointments, name='manage_appointments'),
    # path('delete_appointment/<int:id>/', views.delete_appointment, name='delete_appointment'),
    # path('confirm_appointment/<int:id>/', views.confirm_appointment, name='confirm_appointment'),
    # path('reject_appointment/<int:id>/', views.reject_appointment, name='reject_appointment'),

    # Feedback
#     path('add_feedback/', views.add_feedback, name='add_feedback'),
#     path("feedback/", views.feedback, name="feedback"),
#     path("feedback_success/", views.feedback_success, name="feedback_success"),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('register/addregister', views.addregister, name='addregister'),

    path('login/',views.login,name='login'),
    path('login/addlogin/',views.addlogin, name='addlogin'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),

    path('adminpage/',views.adminpage,name='adminpage'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout),
    
    path('adminpage/logout/',views.logout),
    path('adminpage/add_doctor/',views.add_doctor,name='add_doctor'),
    path('edit_doctor/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('accept_doctor/<int:id>/', views.accept_doctor, name='accept_doctor'),
    path('reject_doctor/<int:id>/', views.reject_doctor, name='reject_doctor'),
    path('adminpage/add_medicine/',views.add_medicine,name='add_medicine'),
    path('edit_medicine/<int:id>/', views.edit_medicine, name='edit_medicine'),
    path('delete_medicine/<int:id>/', views.delete_medicine, name='delete_medicine'),
    
    path('make_appointment/', views.make_appointment, name='make_appointment'),
    path('manage_appointments/', views.manage_appointments, name='manage_appointments'), 
    path('delete_appointment/<int:id>/', views.delete_appointment, name='delete_appointment'),
    path('confirm_appointment/<int:id>/', views.confirm_appointment, name='confirm_appointment'),
    path('reject_appointment/<int:id>/', views.reject_appointment, name='reject_appointment'),
    path('manage_patient/', views.manage_patient, name='manage_patient'),
    path('manage_clinic/', views.manage_clinic, name='manage_clinic'),

    path('register/', views.register, name='register'),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback_success/", views.feedback_success, name="feedback_success"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('user_medicines/', views.user_medicines, name='user_medicines'),
    path('buy_medicine/<int:id>/', views.buy_medicine, name='buy_medicine'),
    path('user_view_payment/', views.user_view_payment, name='user_view_payment'),

    # path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('doctor_tbl/', views.doctor_tbl, name='doctor_tbl'),
    path('doctorpage/', views.doctorpage, name='doctorpage'),
    path('userpage/', views.userpage, name='userpage'),


    path('prescription/', views.prescription, name='prescription'),
    path('add_prescription/', views.add_prescription, name='add_prescription'),
    path('patient_reports/', views.patient_reports, name='patient_reports'),
    path('admin_patient_history/', views.admin_patient_history, name='admin_patient_history'),
    path('doctor_reports/', views.doctor_reports, name='doctor_reports'),
    path('view_payment/', views.view_payment, name='view_payment'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),

    path('doctorpage/upload_test_result/', views.upload_test_result, name='upload_test_result'),
    path('patient_test_results/', views.patient_test_results, name='patient_test_results'),
    path('doctorpage/all_lab_reports/', views.all_lab_reports, name='all_lab_reports'),
    path('user_appointment_history/', views.user_appointment_history, name='user_appointment_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
