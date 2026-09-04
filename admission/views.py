from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

from .models import AdmissionApplication, AcademicDetails
from .forms import AdmissionApplicationForm, AcademicDetailsForm


@login_required
def Admission_Form(request):

    # Check whether the student already has an application
    existing_admission_application = AdmissionApplication.objects.filter(
        student=request.user
    ).first()

    if existing_admission_application:

        return redirect(
            'application_status',
            application_number=existing_admission_application.application_number
        )

    # POST request
    if request.method == 'POST':

        application_form = AdmissionApplicationForm(request.POST)

        academic_form = AcademicDetailsForm(request.POST)

        if application_form.is_valid() and academic_form.is_valid():

            course = application_form.cleaned_data['course']

            # Check whether seats are available
            if course.available_seats <= 0:

                messages.error(
                    request,
                    'Sorry..! No seats available for this course.'
                )

                return redirect('admission_form')

            # Generate Application Number
            application_number = (
                'APP-' +
                get_random_string(
                    8,
                    allowed_chars='0123456789'
                )
            )

            # Save Admission Application
            application = application_form.save(
                commit=False
            )

            application.student = request.user
            application.application_number = application_number
            application.status = 'Pending'

            application.save()

            # Save Academic Details
            academic = academic_form.save(
                commit=False
            )

            academic.application = application

            academic.save()

            # Reduce available seats
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

    # GET request
    else:

        application_form = AdmissionApplicationForm()

        academic_form = AcademicDetailsForm()

    # Display admission form
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