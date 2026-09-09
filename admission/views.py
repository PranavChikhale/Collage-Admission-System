from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

from .models import AdmissionApplication, AcademicDetails, StudentDocuments
from .forms import AdmissionApplicationForm, AcademicDetailsForm, StudentDocumentsForm


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate,Paragraph, Spacer, Table,TableStyle
)


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

            return redirect('documents_upload')


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

    application = get_object_or_404(
        AdmissionApplication,
        application_number=application_number,
        student=request.user
    )

    academic = AcademicDetails.objects.filter(
        application=application
    ).first()

    documents = StudentDocuments.objects.filter(
        application=application
    ).first()

    return render(
        request,
        'admission/application_status.html',
        {
            'application': application,
            'academic': academic,
            'documents': documents,
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

@login_required
def My_Application(request, application_number):

    application = AdmissionApplication.objects.get(
        application_number=application_number,
        student=request.user
    )

    academic = AcademicDetails.objects.filter(
        application=application
    ).first()

    documents = StudentDocuments.objects.filter(
        application=application
    ).first()

    return render(
        request,
        'admission/my_application.html',
        {
            'application': application,
            'academic': academic,
            'documents': documents,
        }
    )

@login_required
def download_application_pdf(request, application_number):

    application = get_object_or_404(
        AdmissionApplication,
        application_number=application_number,
        student=request.user
    )

    academic = AcademicDetails.objects.filter(
        application=application
    ).first()

    documents = StudentDocuments.objects.filter(
        application=application
    ).first()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="Application_{application.application_number}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=colors.HexColor('#d9570e'),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#d9570e'),
        spaceBefore=15,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14
    )

    story = []

    # -----------------------------------------
    # HEADER
    # -----------------------------------------

    story.append(
        Paragraph(
            'COLLEGE ADMISSION MANAGEMENT SYSTEM',
            title_style
        )
    )

    story.append(
        Paragraph(
            'Admission Application',
            subtitle_style
        )
    )

    # -----------------------------------------
    # APPLICATION DETAILS
    # -----------------------------------------

    story.append(
        Paragraph(
            'Application Details',
            heading_style
        )
    )

    application_data = [
        ['Application Number', application.application_number],
        ['Student Name',
         f'{application.student.first_name} {application.student.last_name}'],
        ['Username', application.student.username],
        ['Email', application.student.email],
        ['Course', application.course.course_name],
        ['Course Code', application.course.course_code],
        ['Department', application.course.department],
        [
            'Applied On',
            application.application_date.strftime('%d %b %Y')
        ],
        ['Status', application.status],
    ]

    application_table = Table(
        application_data,
        colWidths=[160, 330]
    )

    application_table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e8')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#222222')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])
    )

    story.append(application_table)

    # -----------------------------------------
    # ACADEMIC DETAILS
    # -----------------------------------------

    if academic:

        story.append(
            Paragraph(
                'Academic Details',
                heading_style
            )
        )

        academic_data = [
            ['10th Percentage', f'{academic.tenth_percentage}%'],
            ['10th College', academic.tenth_collage],
            ['10th Board', academic.tenth_board],
            ['10th Passing Year', str(academic.tenth_passing_year)],
            ['12th Percentage', f'{academic.twelfth_percentage}%'],
            ['12th College', academic.twelfth_collage],
            ['12th Board', academic.twelfth_board],
            ['12th Passing Year', str(academic.twelfth_passing_year)],
        ]

        academic_table = Table(
            academic_data,
            colWidths=[160, 330]
        )

        academic_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e8')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
        )

        story.append(academic_table)

    # -----------------------------------------
    # DOCUMENT DETAILS
    # -----------------------------------------

    if documents:

        story.append(
            Paragraph(
                'Submitted Documents',
                heading_style
            )
        )

        document_data = [
            ['Photo', 'Submitted' if documents.photo else 'Not Submitted'],
            ['Signature', 'Submitted' if documents.signature else 'Not Submitted'],
            [
                '10th Marksheet',
                'Submitted' if documents.tenth_marksheet else 'Not Submitted'
            ],
            [
                '12th Marksheet',
                'Submitted' if documents.twelfth_marksheet else 'Not Submitted'
            ],
            [
                'Leaving Certificate',
                'Submitted' if documents.leaving_certificate else 'Not Submitted'
            ],
            [
                'Caste Certificate',
                'Submitted' if documents.caste_certificate else 'Not Submitted'
            ],
        ]

        document_table = Table(
            document_data,
            colWidths=[220, 270]
        )

        document_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e8')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
        )

        story.append(document_table)

    # -----------------------------------------
    # FOOTER INFORMATION
    # -----------------------------------------

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            'This document is generated electronically by the College '
            'Admission Management System.',
            ParagraphStyle(
                'Footer',
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=8,
                textColor=colors.HexColor('#777777')
            )
        )
    )

    doc.build(story)

    return response

