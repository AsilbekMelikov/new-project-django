from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User

from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Enter password",
                               widget=forms.PasswordInput,
                               )
    password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]

    def clean_password_confirm(self):
        data = self.cleaned_data

        if data["password"] and data["password_confirm"]:
            if data["password"] != data["password_confirm"]:
                raise forms.ValidationError("Your password didn't match, please try again")
        return data["password_confirm"]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]