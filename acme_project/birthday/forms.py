from django import forms
from django.core.exceptions import ValidationError

from .models import Birthday

from .validators import real_age

BEATLES = {"Джон Леннон", "Пол Маккартни", "Джордж Харрисон", "Ринго Старр"}

class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = "__all__"
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
    
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[real_age],
    )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]
    
    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            raise ValidationError(
                "Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!"
            )
        