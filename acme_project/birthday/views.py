from django.shortcuts import render, redirect, get_object_or_404

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown

def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context=context)

def birthday_list(request):
    birthdays = Birthday.objects.all()
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)

# def edit_birthday(request, pk):
#     instance = get_object_or_404(Birthday, pk=pk)
#     form = BirthdayForm(request.POST or None, instance=instance)
#     context = {'form': form}
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday_list.html', context)

