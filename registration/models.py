import io
import os
import uuid

import qrcode
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from s3direct.fields import S3DirectField

image_storage = FileSystemStorage(
    location=u'{0}/logos/'.format(settings.MEDIA_ROOT),
    base_url=u'{0}logos/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    return u'picture/{0}'.format(filename)


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Event Name')
    # logo = models.ImageField(verbose_name='Logo for the event', upload_to=image_directory_path, storage=image_storage)
    logo = S3DirectField(dest='intered-files', max_length=250,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    event_registration_url = models.URLField(verbose_name="Event Registration Link", null=True, blank=True,
                                             max_length=250)
    event_added = models.BooleanField(default=False)
    event_uuid = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.start_date} - {self.end_date})'


@receiver(post_save, sender=Event)
def createUrlLink(sender, instance, created, **kwargs):
    if instance.event_added is False:
        instance.event_uuid = str(uuid.uuid4())[0:4]
        instance.event_registration_url = reverse('register', args=[instance.event_uuid])
        instance.event_added = True
        instance.save()


class ShsTrack(models.Model):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.code


class SchoolList(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    first_name = models.CharField(max_length=200, verbose_name="First Name")
    school = models.ForeignKey(SchoolList, on_delete=models.SET_NULL, blank=True, null=True)
    shs_track = models.ForeignKey(ShsTrack, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name="Current SHS Track")
    projected_course = models.CharField(max_length=200, help_text="First choice of Course", verbose_name="Course", blank=True, null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number", null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    qr_code = models.ImageField(null=True, upload_to='qrcode')
    date_registered = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()
    qr_added = models.BooleanField(default=False)
    registered_event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    grade_level = models.IntegerField(verbose_name="Grade Level", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_registered = timezone.now()
            self.date_modified = timezone.now()
            if self.qr_added is False:
                self.qr_added = True
                self.generate_qrcode()
        return super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,
        )
        qr.add_data(
            f'{self.first_name}|{self.last_name}|{self.email}|{self.mobile}|{self.school}|{self.shs_track}|{self.projected_course}|{self.date_of_birth}|{self.gender}')
        qr.make(fit=True)

        img = qr.make_image()

        buffer = io.BytesIO()
        img.save(buffer)
        buffer.seek(0, os.SEEK_END)
        filename = f'student-{self.last_name}.png'
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.tell(), None)
        self.qr_code.save(filename, filebuffer)

    class Meta:
        ordering = ['id']
