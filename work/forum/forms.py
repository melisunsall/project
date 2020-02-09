from django.contrib.auth.models import User
from django import forms
from .models import Intern, Appointment, Comment, File
from django.forms import DateInput


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SearchForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = ['name']


class EventForm(forms.ModelForm):
    class Meta:
        model = Appointment
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ['user']

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['intern'].queryset = Intern.objects.filter(is_accepted=0)
        self.user = user

    def save(self, commit=True):
        instance = super().save(False)
        instance.user = self.user
        instance.save(commit)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
