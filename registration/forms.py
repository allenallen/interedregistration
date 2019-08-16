from django import forms

from registration.models import Student, SchoolList, SchoolOfficial


class SchoolOfficialRegistrationForm(forms.ModelForm):
    other = forms.CharField(required=False, label="Other")
    class Meta:
        model = SchoolOfficial
        fields = (
            'last_name', 'first_name', 'school', 'course_taken', 'email', 'date_of_birth', 'gender',
            'mobile', 'registered_event', 'designation', 'other')
        widgets = {'registered_event': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(SchoolOfficialRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['school'].required = True

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if SchoolOfficial.objects.filter(email=email).count() > 0:
    #         raise forms.ValidationError("Email already exists")
    #
    #     return email


class RegistrationForm(forms.ModelForm):
    other = forms.CharField(required=False, label="Other")
    otherGrade = forms.IntegerField(required=False, label="Other", max_value=12, min_value=1)

    class Meta:
        model = Student
        fields = (
            'last_name', 'first_name', 'school', 'grade_level', 'shs_track', 'projected_course', 'email',
            'date_of_birth', 'gender',
            'mobile', 'registered_event', 'other', 'otherGrade')
        widgets = {'registered_event': forms.HiddenInput(), 'otherGrade': forms.NumberInput()}

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['school'].required = True
        self.fields['shs_track'].required = True

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if Student.objects.filter(email=email).count() > 0:
    #         raise forms.ValidationError("Email already exists")
    #
    #     return email


class SchoolForm(forms.ModelForm):
    class Meta:
        model = SchoolList
        fields = [
            "name"
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if SchoolList.objects.filter(name__iexact=name).count() > 0:
            raise forms.ValidationError("School is already on the list")

        return name
