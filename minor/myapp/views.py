from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from myapp.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
import time
from .ml_service import ml_service

# Create your views here.
def home(request):
    return render(request, 'home.html')

def appointment(request):
    return render(request, 'appointment.html')

def disease_info(request):
    return render(request,'disease_info.html')

def page1(request):
    return render(request, 'page1.html')

def page2(request):
    return render(request, 'page2.html')

def page3(request):
    return render(request, 'page3.html')

def page4(request):
    return render(request, 'page4.html')

def page5(request):
    return render(request, 'page5.html')

def page6(request):
    return render(request, 'page6.html')

def page7(request):
    return render(request, 'page7.html')

def page8(request):
    return render(request, 'page8.html')

def page9(request):
    return render(request, 'page9.html')

def page10(request):
    return render(request, 'page10.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('login')  # Redirect to a home page or dashboard
        else:
            # The form will automatically pass errors to the template
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Set session start time for timeout tracking
                request.session['last_activity'] = time.time()
                messages.info(request, f"You are now logged in as {username}. Your session will expire in 30 minutes.")
                return redirect('predict') # Redirect to a home page or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home') # Redirect to a home page or login page

@login_required(login_url='login')
def predict(request):
    # Update session activity time
    request.session['last_activity'] = time.time()
    return render(request, 'predict.html')

@login_required(login_url='login')
def camera_capture(request):
    # Update session activity time
    request.session['last_activity'] = time.time()
    return render(request, 'camera_capture.html')

@csrf_exempt
@login_required(login_url='login')
def predict_api(request):
    """API endpoint for ML prediction"""
    if request.method == 'POST':
        try:
            # Update session activity time
            request.session['last_activity'] = time.time()
            
            # Get the uploaded file
            if 'file' not in request.FILES:
                return JsonResponse({'error': 'No file uploaded'}, status=400)
            
            file = request.FILES['file']
            
            # Validate file type
            if not file.content_type.startswith('image/'):
                return JsonResponse({'error': 'File must be an image'}, status=400)
            
            # Get symptom start date
            symptom_start_date = request.POST.get('symptom_start_date')
            
            # Make prediction
            result = ml_service.predict(file, symptom_start_date)
            
            if 'error' in result:
                return JsonResponse(result, status=500)
            
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required(login_url='login')
def result(request):
    # Update session activity time
    request.session['last_activity'] = time.time()
    return render(request, 'result.html')

def check_auth_status(request):
    """API endpoint to check if user is authenticated"""
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True, 'username': request.user.username})
    else:
        return JsonResponse({'authenticated': False})