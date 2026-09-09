from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from admission.models import AdmissionApplication
from .forms import  StudentProfileForm
from .models import  StudentProfile

@login_required
def Profile_View(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'students/profile.html', {'form': form})





@login_required
def view_applications(request):

    applications = AdmissionApplication.objects.filter(student=request.user).select_related('course').order_by('-application_date')

    context = {
        'applications': applications,
    }

    return render(request,'students/view_applications.html',context)