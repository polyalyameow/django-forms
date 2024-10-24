from django.db import models

class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', blank=True, help_text='Необязательное поле', max_length=20)
    birthday = models.DateField('Дата рождения')
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name', 'birthday'],
                name="unique_person_constraint"
            )
        ]