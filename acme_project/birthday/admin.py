from django.contrib import admin
from .models import Tag

admin.site.register(Tag)

# Tag.objects.create(tag='Друг')
# Tag.objects.create(tag='Коллега')
# Tag.objects.create(tag='Родственник')