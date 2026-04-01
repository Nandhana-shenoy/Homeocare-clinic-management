import email
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .models import *
from .models import Appointment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def register(request):

    if request.method == "POST":
        role = request.POST.get('role') 
        username = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('phone')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'msg': 'User already exists'})

        # Create Django User
        user = User.objects.create_user(
            username=username,
            password=password
        )

         # ✅ ROLE CHECK
        if role == "doctor":
            doctor_tbl.objects.create(
    name=name,
    email=email,
    password=password,
    contact=contact,
    address=address
)

            
        else:
            Patient.objects.create(
                user=user,
                contact=contact,
            )

        return redirect('login')

    return render(request, 'register.html')

def addregister(request):
    if request.method == 'POST':
        role = request.POST.get('role')  # Get the selected role from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        contact = request.POST.get('phone')
        
        if role == "doctor":
            user = doctor_tbl(
               name=name,
                email=email,
                password=password,
                contact=contact,
                address=address
            )
            user.save()

        elif role == "user":
            user = user_tbl(   # make sure this model exists
                name=name,
                email=email,
                password=password,
                contact=contact,
                address=address
            )
            user.save()
        return render(request, 'register.html', {'msg': 'Registration Successful'})
    
def login(request):
    return render (request,'login.html')

def adminpage(request):
    return render(request,'adminpage.html')

def addlogin(request):
    email1=request.POST.get('email')
    password1=request.POST.get('password')

    if email1=='admin@gmail.com' and password1=='admin123':
        request.session['admin']='admin'
        return redirect('adminpage')
    
    elif user_tbl.objects.filter(email=email1,password=password1).exists():
        details=user_tbl.objects.get(email=email1,password=password1)
        if details.password==request.POST['password']:
            request.session['uid']=details.id          
        return redirect('userpage')
    
    elif doctor_tbl.objects.filter(email=email1,password=password1).exists():
        details=doctor_tbl.objects.get(email=email1,password=password1)
        if details.password==request.POST['password']:
            request.session['doctor_id']=details.id          
        return redirect('doctorpage')
    
    else:
        return render(request,'login.html',{'msg':'Invalid Email or Password'})

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        # Check if user exists in user_tbl
        user = user_tbl.objects.filter(email=email).first()
        if user:
            return redirect('reset_password', email=email)
            
        # Check if user exists in doctor_tbl
        doctor = doctor_tbl.objects.filter(email=email).first()
        if doctor:
            return redirect('reset_password', email=email)
            
        return render(request, 'forgot_password.html', {'msg': 'Email not found in our records.'})
        
    return render(request, 'forgot_password.html')

def reset_password(request, email):
    if request.method == "POST":
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'msg': 'Passwords do not match.', 'email': email})

        # Update in user_tbl
        user = user_tbl.objects.filter(email=email).first()
        if user:
            user.password = new_password
            user.save()
            return render(request, 'login.html', {'msg': 'Password reset successful. Please login.'})
            
        # Update in doctor_tbl
        doctor = doctor_tbl.objects.filter(email=email).first()
        if doctor:
            doctor.password = new_password
            doctor.save()
            return render(request, 'login.html', {'msg': 'Password reset successful. Please login.'})

        return redirect('login')
        
    return render(request, 'reset_password.html', {'email': email})
# def addlogin(request):
#     email1=request.POST.get('email')
#     password1=request.POST.get('password')
#     if email1=='admin@gmail.com' and password1=='admin123':
#         request.session['admin']='admin'
#         return redirect('adminpage')
    
#     elif user_tbl.objects.filter(email=email1,password=password1).exists():
#         details=user_tbl.objects.get(email=email1,password=password1)
#         if details.password==request.POST['password']:
#             request.session['uid']=details.id          
#         return redirect('index')
        
#     else:
#         return render(request,'login.html',{'msg':'Invalid Email or Password'})

def profile(request):
    selection=user_tbl.objects.all()
    return render(request,'profile.html',{'result':selection})

def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(home)

def add_doctor(request):
    if request.method == 'POST':
        add_doctor_tbl.objects.create(
            name=request.POST.get('name'),
            specialization=request.POST.get('specialization'),
            contact=request.POST.get('contact'),
            email=request.POST.get('email')
        )
        return redirect('add_doctor')

    doctors = add_doctor_tbl.objects.all()
    return render(request, 'add_doctor.html', {'doctors': doctors})

def edit_doctor(request, id):
    doctor = add_doctor_tbl.objects.get(id=id)
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.specialization = request.POST.get('specialization')
        doctor.contact = request.POST.get('contact')
        doctor.email = request.POST.get('email')
        doctor.save()
        return redirect('add_doctor')
    return render(request, 'edit_doctor.html', {'doctor': doctor})

def delete_doctor(request, id):
    doctor = add_doctor_tbl.objects.get(id=id)
    doctor.delete()
    return redirect('add_doctor')

def accept_doctor(request, id):
    doctor = add_doctor_tbl.objects.get(id=id)
    doctor.status = 'Accepted'
    doctor.save()
    return redirect('add_doctor')

def reject_doctor(request, id):
    doctor = add_doctor_tbl.objects.get(id=id)
    doctor.status = 'Rejected'
    doctor.save()
    return redirect('add_doctor')

def add_medicine(request):
    if request.method == 'POST':
        add_medicine_tbl.objects.create(
            medicine_name=request.POST.get('medicine_name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
        )
        return redirect('add_medicine')

    medicines = add_medicine_tbl.objects.all()
    return render(request, 'add_medicine.html', {'medicines': medicines})

def edit_medicine(request, id):
    medicine = add_medicine_tbl.objects.get(id=id)
    if request.method == 'POST':
        medicine.medicine_name = request.POST.get('medicine_name')
        medicine.description = request.POST.get('description')
        medicine.price = request.POST.get('price')
        medicine.stock = request.POST.get('stock')
        medicine.save()
        return redirect('add_medicine')
    return render(request, 'edit_medicine.html', {'medicine': medicine})

def delete_medicine(request, id):
    medicine = add_medicine_tbl.objects.get(id=id)
    medicine.delete()
    return redirect('add_medicine')

def user_medicines(request):
    if 'uid' not in request.session:
        return redirect('login')
    medicines = add_medicine_tbl.objects.all()
    return render(request, 'user_medicines.html', {'medicines': medicines})

def buy_medicine(request, id):
    if 'uid' not in request.session:
        return redirect('login')
    medicine = add_medicine_tbl.objects.get(id=id)
    
    if request.method == 'POST':
        if medicine.stock > 0:
            medicine.stock -= 1
            medicine.save()
            user = user_tbl.objects.get(id=request.session['uid'])
            Payment.objects.create(
                user=user,
                medicine_name=medicine.medicine_name,
                amount=medicine.price,
                card_type=request.POST.get('card_type', 'debit'),
                bank_name=request.POST.get('bank_name', 'Unknown')
            )
            messages.success(request, f"Successfully purchased {medicine.medicine_name}!")
        else:
            messages.error(request, f"Sorry, {medicine.medicine_name} is out of stock.")
        return redirect('user_view_payment')
        
    return render(request, 'medicine_payment.html', {'medicine': medicine})

# userside
from .models import add_doctor_tbl, Appointment

def make_appointment(request):
    doctors = add_doctor_tbl.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        doctor = add_doctor_tbl.objects.get(id=doctor_id)

        if doctor.is_on_leave:
            return render(request, "make_appointment.html", {
                "doctors": doctors,
                "error": "Doctor is on leave. Please book another date."
            })

        Appointment.objects.create(
            doctor=doctor,
            name=request.POST.get("name"),
            gender=request.POST.get("gender"),
            contact=request.POST.get("contact"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            appointment_date=request.POST.get("appointment_date")
        )

        return render(request, "make_appointment.html", {
            "doctors": doctors,
            "success": "Appointment request sent. Waiting for confirmation."
        })

    return render(request, "make_appointment.html", {"doctors": doctors})


def manage_appointments(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'manage_appointments.html', {'appointments': appointments})

def confirm_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = "Confirmed"
    appointment.save()
    return redirect('manage_appointments')


def reject_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = "Rejected"
    appointment.save()
    return redirect('manage_appointments')

def delete_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('manage_appointments')

# def user_login(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Admin Login
#         if email == "admin@gmail.com" and password == "admin123":
#             request.session['admin'] = "admin"
#             return redirect('adminpage')

#         # Normal User Login
#         elif user_tbl.objects.filter(email=email, password=password).exists():
#             user = user_tbl.objects.get(email=email, password=password)
#             request.session['uid'] = user.id
#             return redirect('patient_dashboard')

#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials'})

#     return render(request, 'login.html')
def manage_patient(request):
    patients = Patient.objects.all()
    return render(request, 'manage_patient.html', {'patients': patients})
def manage_clinic(request):
    doctors = add_doctor_tbl.objects.all()
    return render(request, 'manage_clinic.html', {'doctors': doctors})

def user_logout(request):
    logout(request)
    return redirect('login')

from .models import Feedback

def feedback(request):
    if request.method == "POST":
        name = "Anonymous User"
        if 'uid' in request.session:
            try:
                # Use the actual registered patient user_tbl name if logged in
                user = user_tbl.objects.get(id=request.session['uid'])
                name = user.name
            except:
                pass
        
        rating = request.POST.get("rating", None)
        message = request.POST.get("message", "")
        
        rating_val = None
        if rating and rating.isdigit():
            rating_val = int(rating)

        Feedback.objects.create(
            name=name,
            email=None,
            message=message,
            rating=rating_val
        )

        return redirect("feedback_success")

    return render(request, "feedback.html")


def feedback_success(request):
    return render(request, "feedback_success.html")


from django.shortcuts import render, redirect, get_object_or_404
from .models import user_tbl

def user_profile(request):

    if 'uid' not in request.session:
        return redirect('login')

    user = get_object_or_404(user_tbl, id=request.session['uid'])

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.contact = request.POST.get('contact')
        user.address = request.POST.get('address')
        user.password = request.POST.get('password')
        
        user.save()
        return redirect('user_profile')

    return render(request, "user_profile.html", {'user': user})

def doctor_profile(request):
    if 'doctor_id' not in request.session:
        return redirect('login')

    doctor = get_object_or_404(doctor_tbl, id=request.session['doctor_id'])

    if request.method == "POST":
        doctor.name = request.POST.get('name')
        doctor.email = request.POST.get('email')
        doctor.contact = request.POST.get('contact')
        doctor.address = request.POST.get('address')
        doctor.password = request.POST.get('password')
        
        doctor.save()
        return redirect('doctor_profile')

    return render(request, "doctor_profile.html", {'doctor': doctor})
# def home(request):
#     return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')


def doctorpage(request):
    return render(request, 'doctorpage.html')

def userpage(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        user = user_tbl.objects.get(id=uid)
        return render(request, 'userpage.html', {'user': user})
    else:
        return redirect('login')


from .models import Prescription
from datetime import date

def add_prescription(request):
    if request.method == "POST":
        doctor_name_val = "Unknown Doctor"
        if 'doctor_id' in request.session:
            doc = doctor_tbl.objects.filter(id=request.session['doctor_id']).first()
            if doc:
                doctor_name_val = doc.name
        elif request.user.is_authenticated:
            doctor_name_val = request.user.username

        patient_user = request.user if request.user.is_authenticated else None
        
        age_input = request.POST.get('age')
        age_val = int(age_input) if age_input and age_input.isdigit() else None

        Prescription.objects.create(
            patient=patient_user,
            patient_name=request.POST.get('patient_name'),
            doctor_name=doctor_name_val,
            age=age_val,
            gender=request.POST.get('gender'),
            diagnosis=request.POST.get('diagnosis'),
            medicines=request.POST.get('medicines'),
            advice=request.POST.get('advice'),
            report_file=request.FILES.get('report_file'),
            other_report=request.FILES.get('other_report'),
            status="Completed"
        )
        return redirect('add_prescription')

    patients = user_tbl.objects.all()
    return render(request, 'prescription.html', {'patients': patients})


def prescription(request):
    patients = user_tbl.objects.all()
    return render(request, 'prescription.html', {'patients': patients})


def patient_reports(request):
    if 'uid' not in request.session:
        return redirect('login')

    try:
        user = user_tbl.objects.get(id=request.session['uid'])
        # Use icontains and split mapping to ensure backwards compatibility with manually typed inputs
        first_name = user.name.split(' ')[0]
        prescriptions = Prescription.objects.filter(patient_name__icontains=first_name)
    except user_tbl.DoesNotExist:
        prescriptions = []
        
    return render(request, 'patient_reports.html', {'prescriptions': prescriptions, 'user': user})

def admin_patient_history(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'admin_patient_history.html', {'prescriptions': prescriptions})

def doctor_reports(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'doctor_reports.html', {'prescriptions': prescriptions})

def view_payment(request):
    payments = Payment.objects.all().order_by('-date')
    return render(request, 'view_payment.html', {'payments': payments})

def user_view_payment(request):
    if 'uid' not in request.session:
        return redirect('login')
    user = user_tbl.objects.get(id=request.session['uid'])
    payments = Payment.objects.filter(user=user).order_by('-date')
    return render(request, 'user_view_payment.html', {'payments': payments})

def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks})


def upload_test_result(request):
    if 'doctor_id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        uid = request.POST.get('patient_id')
        user = user_tbl.objects.get(id=uid)
        doctor = doctor_tbl.objects.get(id=request.session['doctor_id'])

        MedicalTestResult.objects.create(
            user=user,
            test_name=request.POST.get('test_name'),
            test_date=request.POST.get('test_date'),
            result_file=request.FILES.get('result_file'),
            uploaded_by=doctor,
            description=request.POST.get('description')
        )
        messages.success(request, "Test Result uploaded successfully!")
        return redirect('upload_test_result')

    patients = user_tbl.objects.all()
    return render(request, 'upload_test_result.html', {'patients': patients})


def patient_test_results(request):
    if 'uid' not in request.session:
        return redirect('login')

    user = user_tbl.objects.get(id=request.session['uid'])
    
    # Lab results from the specific MedicalTestResult model
    results = MedicalTestResult.objects.filter(user=user).order_by('-test_date')
    
    # Reports from the Prescription model (matching by name since some prescriptions don't have a direct link)
    first_name = user.name.split(' ')[0]
    prescription_reports = Prescription.objects.filter(patient_name__icontains=first_name).exclude(report_file='')
    
    return render(request, 'patient_test_results.html', {
        'results': results, 
        'prescription_reports': prescription_reports,
        'user': user
    })


def all_lab_reports(request):
    if 'doctor_id' not in request.session:
        return redirect('login')
    
    results = MedicalTestResult.objects.all().order_by('-test_date')
    return render(request, 'all_lab_reports.html', {'results': results})

def user_appointment_history(request):
    if 'uid' not in request.session:
        return redirect('login')
    
    user = user_tbl.objects.get(id=request.session['uid'])
    # Filter appointments by email since that's more unique than name
    appointments = Appointment.objects.filter(email=user.email).order_by('-appointment_date')
    
    return render(request, 'user_appointment_history.html', {
        'appointments': appointments,
        'user': user
    })
