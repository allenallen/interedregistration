import json
from datetime import date

from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from excel_response import ExcelResponse

from intered import settings
from registration.forms import RegistrationForm, SchoolForm
from registration.models import Event, Student, SchoolList
from django.views.decorators.csrf import csrf_exempt

import after_response


@after_response.enable
def extractStudents(request):
    print('HERE')
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
    print(data)
    return ExcelResponse(data, 'students')


def registration(request, uuid):
    print('HERE')
    print(request.method)
    print(uuid)
    event = get_object_or_404(Event, event_uuid=uuid)
    if request.method == 'POST':
        print('HERE POST')
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            print('HERE VALID')
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            school = form.cleaned_data['school']
            shs_track = form.cleaned_data['shs_track']
            projected_course = form.cleaned_data['projected_course']
            email = form.cleaned_data['email']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            mobile = form.cleaned_data['mobile']

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
            student.save()

            html_message = render_to_string('email_template.html',
                                            context={'last_name': student.last_name, 'first_name': student.first_name,
                                                     'school': student.school})
            print(html_message)
            msg = EmailMessage(subject='Thank You', body=html_message, from_email=settings.DEFAULT_FROM_EMAIL,
                               to=[student.email],
                               cc=[settings.EMAIL_CC])

            msg.attach(student.qr_code.name, student.qr_code.read(), 'image/png')

            msg.content_subtype = 'html'
            msg.send()

            return render(request, 'success.html', context={'student': student,
                                                            'event_name': event.name,
                                                            'event_id': event.id,
                                                            'event_logo': event.logo,
                                                            'event_uuid': event.event_uuid})
    else:
        form = RegistrationForm()

    is_expired = date.today() > event.end_date

    context = {
        'event_name': event.name,
        'event_id': event.id,
        'event_logo': event.logo,
        'event_start_date': event.start_date,
        'event_end_date': event.end_date,
        'form': form,
        'is_expired': is_expired
    }
    print(context)
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
