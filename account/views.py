from django.contrib.auth import authenticate , login , logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                # Superuser → Custom Admin Dashboard
                if user.is_superuser:
                    return redirect('admin_dashboard')

                # Admin / Student → Based on UserProfile role
                if hasattr(user, 'userprofile'):
                    if user.userprofile.role == 'admin':
                        return redirect('admin_dashboard')

                    elif user.userprofile.role == 'student':
                        return redirect('student_dashboard')

                return redirect('home')

            else:
                return render(
                    request,
                    'account/login.html',
                    {
                        'form': form,
                        'error': 'Invalid username or password'
                    }
                )

    else:
        form = LoginForm()

    return render(
        request,
        'account/login.html',
        {'form': form}
    )

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return render(
                    request,
                    'account/register.html',
                    {
                        'form': form,
                        'error': 'Passwords do not match'
                    }
                )

            if User.objects.filter(username=username).exists():
                return render(
                    request,
                    'account/register.html',
                    {
                        'form': form,
                        'error': 'Username already exists'
                    }
                )

            if User.objects.filter(email=email).exists():
                return render(
                    request,
                    'account/register.html',
                    {
                        'form': form,
                        'error': 'Email already exists'
                    }
                )

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            messages.success(
                request,
                'Registration successful. Please login.'
            )

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'account/register.html',
        {'form': form}
    )


@login_required
def STUDENT_DASHBOARD(request):
    return render(request, 'students/student_dashboard.html')

@login_required
def ADMIN_DASHBORAD(request):
    return render(request, 'admin/admin_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def HOME(request):
    return render(request, 'home.html')
