from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Teacher
from django.core.exceptions import ValidationError
from django.utils import timezone


class TeacherLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    school_level = forms.ChoiceField(choices=[('primary', 'Primary School'), ('secondary', 'Secondary School')])


class TeacherRegistrationForm(UserCreationForm):
    """
    Custom registration form for teachers that extends Django's UserCreationForm
    Includes all fields from Teacher model with custom validation
    """
    
    # Custom date field with HTML5 date input
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: YYYY-MM-DD"
    )
    
    class Meta:
        model = Teacher  # Uses our custom Teacher model
        fields = [  # Fields to include in the form, in order
            'username', 'email',
            'first_name', 'last_name', 'tsc_number', 'gender',
            'date_of_birth', 'phone_number', 'qualification',
            'subjects_taught', 'current_school', 'school_level', 'district',
            'region', 'profile_picture'
        ]
    
    def clean_date_of_birth(self):
        """Validate that teacher is at least 18 years old"""
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            age = (timezone.now().date() - dob).days // 365
            if age < 18:
                raise ValidationError("You must be at least 18 years old.")
        return dob
    
    def clean_tsc_number(self):
        """Validate that TSC number is unique"""
        tsc_number = self.cleaned_data.get('tsc_number')
        if Teacher.objects.filter(tsc_number=tsc_number).exists():
            raise ValidationError("This TSC number is already registered.")
        return tsc_number