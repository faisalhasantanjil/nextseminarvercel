from .models import *
from django.forms import ModelForm, DateTimeInput, DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class SeminarForm(ModelForm):

    class Meta:
        model = Seminar
        exclude = ("organization",)
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'date'}),
            'start_time': DateTimeInput(attrs={'type': 'time'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'end_time': DateInput(attrs={'type': 'time'})
        }


class UserInformationForm(ModelForm):

    class Meta:
        model = UserInformation
        exclude = ("user",)


class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        exclude = ("user",)


class RegistrationForm(ModelForm):

    class Meta:
        model = Registration
        fields = '__all__'
