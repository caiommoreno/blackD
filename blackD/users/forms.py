from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .choices import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, min_length=2, label='usuario',
                               widget=forms.TextInput(
                                    attrs={
                                        "placeholder": "Digite aqui",
                                        "class": "form-control"
                                    }
                                ))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(
                                attrs={
                                    "placeholder" : "Digite aqui",
                                    "class": "form-control"
                                }
                            ))

    password1 = forms.CharField(label='Senha', max_length=50, min_length=2,
                                widget=forms.PasswordInput(
                                    attrs={
                                        "placeholder": "Digite aqui",
                                        "class": "form-control"
                                    }
                                ))
    password2 = forms.CharField(label='Confirme sua senha', max_length=50, min_length=2,
                                widget=forms.PasswordInput(
                                    attrs={
                                        "placeholder": "Digite aqui",
                                        "class": "form-control"
                                    }
                                ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()    
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    sex = forms.ChoiceField(choices = SEX_CHOICES, required=True)
    class Meta:
        model = Profile
        fields = ['image', 'sex']
