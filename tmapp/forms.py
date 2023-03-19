from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Project, Task, Sprint


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", "key")


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("project", "sprint", "title", "body", "state", "executor")


class AddSprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ("project", "title", "target", "duration", "sprint_start")
