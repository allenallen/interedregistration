from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from intered import settings
from registration.forms import RegistrationForm
from registration.models import Event, Student


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

    context = {
        'event_name': event.name,
        'event_id': event.id,
        'event_logo': event.logo,
        'event_start_date': event.start_date,
        'event_end_date': event.end_date,
        'form': form
    }
    print(context)
    return render(request, 'registration.html', context=context)
