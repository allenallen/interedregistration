import json
from datetime import date
from smtplib import SMTPException, SMTPSenderRefused

from django.core.mail import get_connection, send_mail, EmailMultiAlternatives, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from excel_response import ExcelResponse

from intered import settings
from registration.forms import RegistrationForm, SchoolForm, SchoolOfficialRegistrationForm
from registration.models import Event, Student, SchoolList, SchoolOfficial
from django.views.decorators.csrf import csrf_exempt

import after_response

COURSES = (
    ('Accounting', 'Accounting'), ('Bartending', 'Bartending'), ('Dentistry', 'Dentistry'),
    ('Engineering(Industrial)', 'Engineering(Industrial)'), ('Tourism', 'Tourism'), ('Journalism', 'Journalism'),
    ('IT', 'IT'), ('Legal Management', 'Legal Management'), ('Psychology', 'Psychology'),
    ('Diplomacy/Foreign Service', 'Diplomacy/Foreign Service'),
    ('Business Administration', 'Business Administration'), ('Dressmaking', 'Dressmaking'),
    ('Management', 'Management'),
    ('Military School', 'Military School'), ('HRM', 'HRM'),
    ('Music Performance & Prod\'n', 'Music Performance & Prod\'n'),
    ('Education - Early, Secondary, SPED', 'Education - Early, Secondary, SPED'),
    ('Pilot(Private & Commercial)', 'Pilot(Private & Commercial'),
    ('Engineering(Civil)', 'Engineering(Civil)'), ('Animation', 'Animation'),
    ('Engineering(Computer)', 'Engineering(Computer)'),
    ('Radiology', 'Radiology'), ('Architecture', 'Architecture'), ('Chemistry', 'Chemistry'),
    ('Engineering(General)', 'Engineering(General)'),
    ('Fine Arts', 'Fine Arts'), ('Computer Science & Programming', 'Computer Science & Programming'),
    ('Occupational Therapy', 'Occupational Therapy'),
    ('Marine Transportation & Seafaring', 'Marine Transportation & Seafaring'), ('Optometry', 'Optometry'),
    ('Nursing', 'Nursing'),
    ('Plumbing', 'Plumbing'), ('Med Tech', 'Med Tech'), ('Police', 'Police'), ('Medicine', 'Medicine'),
    ('Geology', 'Geology'),
    ('Housekeeping', 'Housekeeping'), ('Actuarial Science', 'Actuarial Science'),
    ('Culinary Arts & Chef Studies', 'Culinary Arts & Chef Studies'),
    ('Agriculture', 'Agriculture'),
    ('Aeronautical Aviation Engineering & Maintenance', 'Aeronautical Aviation Engineering & Maintenance'),
    ('Cruise Line', 'Cruise Line'), ('Engineering(Mechanical)', 'Engineering(Mechanical)'),
    ('Interior Design', 'Interior Design'),
    ('Marketing', 'Marketing'), ('Economics', 'Economics'),
    ('English & Communication Arts', 'English & Communication Arts'),
    ('Bread & Pastry', 'Bread & Pastry'), ('Banking & Finance', 'Banking & Finance'), ('Broadcasting', 'Broadcasting'),
    ('Mass Communications', 'Mass Communication'), ('Customs', 'Customs'), ('Political Science', 'Political Science'),
    ('Design', 'Design'),
    ('Biology', 'Biology'), ('Human Resources', 'Human Resources'), ('Entrepreneurship', 'Entrepreneurship'),
    ('Maths', 'Maths'),
    ('Engineering(Electrical)', 'Engineering(Electrical)'), ('Social Worker', 'Social Worker'),
    ('Criminology', 'Criminology'),
    ('Speech Pathologist', 'Speech Pathologist'), ('Engineering(Electronics)', 'Engineering(Electronics)'),
    ('Advertising', 'Advertising'),
    ('Multimedia', 'Multimedia'), ('Public Health & Admin', 'Public Health & Admin'), ('Pharmacy', 'Pharmacy'),
    ('Physics', 'Physics'),
    ('Law', 'Law'), ('Engineering(Petroleum)', 'Engineering(Petroleum)'),
    ('Engineering(Chemical)', 'Engineering(Chemical)'),
    ('Environmental Studies', 'Environmental Studies'),
    ('Information and Communication Technology', 'Information and Communication Technology'),
    ('Biochemistry', 'Biochemistry'), ('Veterinary Science', 'Veterinary Science'),
    ('Engineering(ECE)', 'Engineering(ECE)'),
    ('Automotive & Motor Cycle', 'Automotive & Motor Cycle'), ('Fashion', 'Fashion'),
    ('Make Up & Hair Dressing', 'Make UP & Hair Dressing'),
    ('Guidance & Counseling', 'Guidance & Counseling'), ('Physical Therapy', 'Physical Therapy'),
    ('History', 'History'),
    ('Food Technology & Nutrition', 'Food Technology & Nutrition'), ('Public Health', 'Public Health'),
    ('Flight Attendant', 'Flight Attendant'),
    ('Sports', 'Sports'), ('Humanities', 'Humanities'), ('OTHER', 'Other (Please specify)')
)

GRADE_LEVEL = (
    ('10', '10'), ('11', '11'), ('12', '12'), (0, 'Other')
)


@after_response.enable
def extractStudents(request):
    print('Extracting Students')
    students = Student.objects.values_list('last_name', 'first_name', 'school__name', 'shs_track__code',
                                           'projected_course', 'email', 'mobile', 'date_of_birth', 'gender')

    data = [['', 'Last Name', 'First Name', 'Current School', 'Track', 'Projected Course', 'Email', 'Mobile Number',
             'Birthday', 'Gender']]

    count = 0
    for student in students:
        count += 1
        # data += [[str(count), student.last_name, student.first_name, student.school.name, student.shs_track.code,
        #           student.projected_course, student.email, student.mobile, student.date_of_birth, student.gender]]
        data += [[str(count), student[0], student[1], student[2], student[3],
                  student[4], student[5], student[6], student[7], student[8]]]

    return ExcelResponse(data, 'students')


def registration_school_official(request, uuid):
    print('GET form')

    event = get_object_or_404(Event, event_uuid=uuid)
    if request.method == 'POST':
        print('Form POST')
        form = SchoolOfficialRegistrationForm(request.POST, event_uuid=uuid)

        if form.is_valid():
            print('VALID')
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            school = form.cleaned_data['school']
            # projected_course = form.cleaned_data['projected_course']
            email = form.cleaned_data['email']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            mobile = form.cleaned_data['mobile']
            print(form.cleaned_data['course_taken'])
            if form.cleaned_data['course_taken'] == 'OTHER':
                print('OTHER')
                course_taken = form.cleaned_data['other']
            else:
                course_taken = form.cleaned_data['course_taken']

            schoolOfficial = SchoolOfficial()
            schoolOfficial.last_name = last_name
            schoolOfficial.first_name = first_name
            schoolOfficial.school = school
            schoolOfficial.course_taken = course_taken
            schoolOfficial.email = email
            schoolOfficial.date_of_birth = date_of_birth
            schoolOfficial.gender = gender
            schoolOfficial.mobile = mobile
            schoolOfficial.registered_event = event
            schoolOfficial.save()

            html_message = render_to_string('email_template.html',
                                            context={'last_name': schoolOfficial.last_name,
                                                     'first_name': schoolOfficial.first_name,
                                                     'school': schoolOfficial.school})

            try:
                msg = EmailMessage(subject='Thank You', body=html_message, from_email=settings.EMAIL_HOST_USER,
                                   to=[schoolOfficial.email],
                                   cc=[settings.EMAIL_CC, settings.EMAIL_CC_1])

                msg.attach(schoolOfficial.qr_code.name, schoolOfficial.qr_code.read(), 'image/png')
                msg.content_subtype = 'html'
                msg.send(fail_silently=False)
            except Exception as e:
                try:
                    msg = EmailMessage(subject='Thank You', body=html_message, from_email=settings.EMAIL_HOST_USER_BACKUP1,
                                       to=[schoolOfficial.email],
                                       cc=[settings.EMAIL_CC, settings.EMAIL_CC_1])

                    msg.attach(schoolOfficial.qr_code.name, schoolOfficial.qr_code.read(), 'image/png')
                    msg.content_subtype = 'html'
                    connection = get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER_BACKUP1,
                    password=settings.EMAIL_HOST_PASSWORD,
                    )
                    msg.send(connection)
                except Exception as e:
                    msg = EmailMessage(subject='Thank You', body=html_message, from_email=settings.EMAIL_HOST_USER_BACKUP2,
                                       to=[schoolOfficial.email],
                                       cc=[settings.EMAIL_CC, settings.EMAIL_CC_1])

                    msg.attach(schoolOfficial.qr_code.name, schoolOfficial.qr_code.read(), 'image/png')
                    msg.content_subtype = 'html'
                    connection = get_connection(
                        host=settings.EMAIL_HOST_BACKUP,
                        port=settings.EMAIL_PORT,
                        username=settings.EMAIL_HOST_USER_BACKUP2,
                        password=settings.EMAIL_HOST_USER_BACKUP_PASSWORD,
                    )
                    msg.send(connection)

            return render(request, 'success.html', context={'official': schoolOfficial,
                                                            'event_name': event.name,
                                                            'event_id': event.id,
                                                            'event_logo': event.logo,
                                                            'event_uuid': event.event_uuid})
    else:
        form = SchoolOfficialRegistrationForm(event_uuid=uuid)

    is_expired = date.today() > event.end_date

    context = {
        'event_uuid': event.event_uuid,
        'event_name': event.name,
        'event_id': event.id,
        'event_logo': event.logo,
        'event_start_date': event.start_date,
        'event_end_date': event.end_date,
        'form': form,
        'is_expired': is_expired,
        'courses': sorted(COURSES),
    }
    return render(request, 'registration_school_official.html', context=context)


def registration(request, uuid):
    print('Get FORM')
    event = get_object_or_404(Event, event_uuid=uuid)
    if request.method == 'POST':
        print('Form POST')
        form = RegistrationForm(request.POST, event_uuid=uuid)

        if form.is_valid():
            print('HERE VALID')
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            school = form.cleaned_data['school']
            shs_track = form.cleaned_data['shs_track']
            # projected_course = form.cleaned_data['projected_course']
            email = form.cleaned_data['email']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            mobile = form.cleaned_data['mobile']
            print(form.cleaned_data['projected_course'])
            print(form.cleaned_data['grade_level'])
            if form.cleaned_data['projected_course'] == 'OTHER':
                print('OTHER')
                projected_course = form.cleaned_data['other']
                print(projected_course)
            else:
                projected_course = form.cleaned_data['projected_course']

            if form.cleaned_data['grade_level'] == 0:
                print('OTHER')
                grade_level = form.cleaned_data['otherGrade']
                print(grade_level)
            else:
                grade_level = form.cleaned_data['grade_level']

            student = Student()
            student.last_name = last_name
            student.first_name = first_name
            student.school = school
            student.shs_track = shs_track
            student.projected_course = projected_course
            student.email = email
            student.date_of_birth = date_of_birth
            student.gender = gender
            student.mobile = mobile
            student.registered_event = event
            student.grade_level = grade_level
            student.save()

            html_message = render_to_string('email_template.html',
                                            context={'last_name': student.last_name, 'first_name': student.first_name,
                                                     'school': student.school})

            msg = EmailMessage(subject='Thank You', body=html_message, from_email=settings.DEFAULT_FROM_EMAIL,
                               to=[student.email],
                               cc=[settings.EMAIL_CC, settings.EMAIL_CC_1])

            msg.attach(student.qr_code.name, student.qr_code.read(), 'image/png')
            # change
            msg.content_subtype = 'html'

            try:
                msg.send(fail_silently=False)
            except:
                connection = get_connection(
                    host=settings.EMAIL_HOST_BACKUP,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER_BACKUP1,
                    password=settings.EMAIL_HOST_USER_BACKUP_PASSWORD,
                )
                msg.send(connection)

            return render(request, 'success.html', context={'student': student,
                                                            'event_name': event.name,
                                                            'event_id': event.id,
                                                            'event_logo': event.logo,
                                                            'event_uuid': event.event_uuid})
    else:
        form = RegistrationForm(event_uuid=uuid)

    is_expired = date.today() > event.end_date

    context = {
        'event_uuid': event.event_uuid,
        'event_name': event.name,
        'event_id': event.id,
        'event_logo': event.logo,
        'event_start_date': event.start_date,
        'event_end_date': event.end_date,
        'form': form,
        'is_expired': is_expired,
        'courses': sorted(COURSES),
        'grade_level': GRADE_LEVEL
    }

    return render(request, 'registration.html', context=context)


def SchoolNewPopup(request):
    form = SchoolForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_school");</script>' % (instance.pk, instance))

    return render(request, "school_form.html", {"form": form})


@csrf_exempt
def get_school_id(request):
    if request.is_ajax():
        school_name = request.GET['school_name']
        school_id = SchoolList.objects.get(name=school_name).id
        data = {'id': school_id}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")
