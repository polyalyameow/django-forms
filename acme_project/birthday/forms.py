from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Birthday, Congratulation, Tag

from .validators import real_age

BEATLES = {"Джон Леннон", "Пол Маккартни", "Джордж Харрисон", "Ринго Старр"}

class BirthdayForm(forms.ModelForm):
    
    class Meta:
        model = Birthday
        fields = "__all__"
        exclude = ('author',)
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
    
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[real_age],
    )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Clear existing tags to avoid duplicates
        instance.tags.clear()  

        # Process tags from the form
        tags = self.cleaned_data.get('tags', [])
        for tag in tags:
            tag_instance, created = Tag.objects.get_or_create(tag=tag)
            instance.tags.add(tag_instance)

        if commit:
            instance.save()
        return instance

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]
    
    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                "Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!"
            )

class CongratulationForm(forms.ModelForm):
    class Meta:
        model = Congratulation
        fields = ('text',) 