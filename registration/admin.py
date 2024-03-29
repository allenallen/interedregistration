import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Student, SchoolList, Event, ShsTrack, SchoolOfficial


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(SchoolOfficial)
class SchoolOfficialAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id', 'last_name', 'first_name', 'school', 'designation', 'course_taken', 'email', 'date_of_birth', 'mobile',
        'gender', 'date_registered', 'registered_event')
    list_filter = ('registered_event', 'school',)
    actions = ['export_as_csv']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id', 'last_name', 'first_name', 'school', 'grade_level', 'shs_track', 'projected_course', 'email',
        'date_of_birth', 'mobile',
        'gender', 'date_registered', 'registered_event')
    actions = ['export_as_csv']
    list_filter = ('registered_event', 'school',)
    change_list_template = 'change_list.html'
    search_fields = ('first_name', 'last_name', 'email')


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

    readonly_fields = ('event_registration_url',)


admin.site.register(SchoolList)
admin.site.register(ShsTrack)
