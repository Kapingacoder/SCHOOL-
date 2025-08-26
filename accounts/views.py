from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from .forms import TeacherRegistrationForm, TeacherLoginForm
from .models import Teacher
from django.contrib import messages


def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            school_level = form.cleaned_data['school_level']
            
            # Hapa tunatumia `authenticate` ambayo inapaswa kurejesha `Teacher` object
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Kwa kuwa `user` ni `Teacher` object, tunafikia `school_level` moja kwa moja
                if user.school_level == school_level:
                    login(request, user)
                    messages.success(request, f'Karibu, {user.get_full_name()}!')
                    
                    if school_level == 'primary':
                        return redirect('primary_dashboard:dashboard')
                    elif school_level == 'secondary':
                        return redirect('secondary_dashboard:dashboard')
                else:
                    messages.error(request, 'Kiwango cha shule ulichochagua si sahihi kwa akaunti yako.')
            else:
                messages.error(request, 'Jina la mtumiaji au nywila si sahihi.')
        else:
            messages.error(request, 'Tafadhali sahihisha makosa hapa chini.')
    else:
        form = TeacherLoginForm()
    return render(request, 'accounts/teacher_login.html', {'form': form})

def teacher_register(request):
    """
    Handles teacher registration:
    Handles teacher registration:
    - Shows empty form on GET request
    - Processes form data on POST request
    - Logs in user after successful registration
    """
    
    if request.method == 'POST':
        # Create form instance with submitted data and files
        form = TeacherRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the new teacher
            user = form.save()
            
            # Log the user in
            login(request, user)
            
            # Success message
            messages.success(request, 'Registration successful!')
            
            # Redirect to login page
            return redirect('accounts:teacher_login')
        else:
            print(form.errors)  
    else:
        # Create empty form for GET request
        form = TeacherRegistrationForm()
    
    # Render the template with the form
    return render(request, 'accounts/teacher_register.html', {'form': form})

def teacher_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:teacher_login')

def primary_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'teacher') or request.user.teacher.school_level != 'primary':
        return redirect('teacher_login')
    return redirect('primary_dashboard:dashboard')

def secondary_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'teacher') or request.user.teacher.school_level != 'secondary':
        return redirect('teacher_login')
    return redirect('secondary_dashboard:dashboard')
