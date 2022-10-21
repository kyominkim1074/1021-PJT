from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
        )
