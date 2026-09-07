from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

from .models import AdmissionApplication, AcademicDetails, StudentDocuments
from .forms import AdmissionApplicationForm, AcademicDetailsForm, StudentDocumentsForm


@login_required
def Admission_Form(request):

    if request.method == 'POST':

        application_form = AdmissionApplicationForm(request.POST)
        academic_form = AcademicDetailsForm(request.POST)

        if application_form.is_valid() and academic_form.is_valid():

            course = application_form.cleaned_data['course']

            if course.available_seats <= 0:
                messages.error(
                    request,
                    'Sorry..! No seats available for this course.'
                )
                return redirect('admission_form')

            application_number = (
                'APP-' +
                get_random_string(
                    8,
                    allowed_chars='0123456789'
                )
            )

            application = application_form.save(commit=False)
            application.student = request.user
            application.application_number = application_number
            application.status = 'Pending'
            application.save()

            academic = academic_form.save(commit=False)
            academic.application = application
            academic.save()

            course.available_seats -= 1
            course.save()

            messages.success(
                request,
                'Your Application Submitted Successfully...!!!'
            )

            return redirect(
                'application_status',
                application_number=application.application_number
            )

    else:
        application_form = AdmissionApplicationForm()
        academic_form = AcademicDetailsForm()

    return render(
        request,
        'admission/admission_form.html',
        {
            'application_form': application_form,
            'academic_form': academic_form,
        }
    )


@login_required
def Admission_Status(request, application_number):

    application = AdmissionApplication.objects.get(
        application_number=application_number,
        student=request.user
    )

    academic = AcademicDetails.objects.filter(
        application=application
    ).first()

    return render(
        request,
        'admission/application_status.html',
        {
            'application': application,
            'academic': academic,
        }
    )

@login_required
def documents_upload(request):
    application = AdmissionApplication.objects.filter(student=request.user).first()

    if not application:
        messages.error(request, "Please Submit Your Addmission Application  First....!")
        return redirect('admission_form')
    documents, created = StudentDocuments.objects.get_or_create( application=application)
    if request.method == 'POST':
        form = StudentDocumentsForm(request.POST, request.FILES, instance=documents)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Document Submitted Successfully...!!!"
            )
            return redirect('application_status', application_number=application.application_number)
    else:
        form = StudentDocumentsForm(instance=documents)
        return render(request,'admission/documents_upload.html',{'form':form,'application':application})

@login_required
def admin_applications(request):
    if not (
        request.user.is_superuser
        or hasattr(request.user, 'userprofile')
        and request.user.userprofile.role == 'admin'
    ):
        return redirect('home')

    applications = AdmissionApplication.objects.all().select_related(
        'student',
        'course'
    )

    return render(
        request,
        'admission/admin_application.html',
        {'applications': applications}
    )

@login_required
def admin_application_detail(request, application_number):
    if not (
        request.user.is_superuser
        or (
            hasattr(request.user, 'userprofile')
            and request.user.userprofile.role == 'admin'
        )
    ):
        return redirect('home')

    application = AdmissionApplication.objects.get(
        application_number=application_number
    )

    academic = AcademicDetails.objects.filter(
        application=application
    ).first()

    documents = StudentDocuments.objects.filter(
        application=application
    ).first()

    return render(
        request,
        'admission/admin_application_detail.html',
        {
            'application': application,
            'academic': academic,
            'documents': documents,
        }
    )