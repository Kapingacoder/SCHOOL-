from django.urls import path
from .views import teacher_register, teacher_login, teacher_logout

app_name = 'accounts'

urlpatterns = [
    path('register/', teacher_register, name='teacher_register'),
    path('login/', teacher_login, name='teacher_login'),
    path('logout/', teacher_logout, name='teacher_logout'),  # Added logout URL
]
