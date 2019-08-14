import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Student, SchoolList, Event, ShsTrack


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


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id', 'last_name', 'first_name', 'school', 'grade_level', 'shs_track', 'projected_course', 'email',
        'date_of_birth', 'mobile',
        'gender', 'date_registered', 'registered_event')
    actions = ['export_as_csv']
    list_filter = ('registered_event', 'school',)
    change_list_template = 'change_list.html'


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
