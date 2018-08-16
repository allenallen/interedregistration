from django.contrib import admin
from .models import Student, SchoolList, Event, ShsTrack


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'last_name', 'first_name', 'school', 'shs_track', 'projected_course', 'email',
        'date_of_birth', 'mobile',
        'gender', 'date_registered')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')

    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'event_registration_url')
        }),
        ('Event Date', {
            'fields': ('start_date', 'end_date')
        }),
    )


admin.site.register(SchoolList)
admin.site.register(ShsTrack)
