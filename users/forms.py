from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'name', 'email', 'first_name', 'last_name', 'password1', 'password2', ]

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if User.objects.filter(name=name):
            raise forms.ValidationError("Name already exists")
        return name