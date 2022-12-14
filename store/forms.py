from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ShippingAddress


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }
    ))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        }
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя пользователя'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия пользователя'
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Логин пользователя'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email пользователя'
                }
            ),
        }


class CustomerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

        widgets = {
            'address': forms.TextInput(
                attrs={
                    "class": 'form-control',
                    'placeholder': 'Адрес'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    "class": 'form-control',
                    'placeholder': 'Город'
                }
            ),
            'state': forms.TextInput(
                attrs={
                    "class": 'form-control',
                    'placeholder': 'Регион'
                }
            ),
            'zipcode': forms.TextInput(
                attrs={
                    "class": 'form-control',
                    'placeholder': 'Индекс'
                }
            )

        }


class SendCommentForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            "class": 'email_form-input flex-grow-1 mb-3',
            'placeholder': 'Email..'
        }
    ))
    comment = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'text_form-input flex-grow-1 mb-3',
            'placeholder': 'Оставьте отзыв'
        }
    ))
