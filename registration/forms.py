from django import forms

from registration.models import Student, SchoolList


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'last_name', 'first_name', 'school', 'shs_track', 'projected_course', 'email', 'date_of_birth', 'gender',
            'mobile')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['school'].required = True
        self.fields['shs_track'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("Email already exists")

        return email


class SchoolForm(forms.ModelForm):
    class Meta:
        model = SchoolList
        fields = [
            "name"
        ]

