from django import forms

from registration.models import Student


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'last_name', 'first_name', 'school', 'shs_track', 'projected_course', 'email', 'date_of_birth', 'gender',
            'mobile')
