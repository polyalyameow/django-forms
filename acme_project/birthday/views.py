from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown

class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user 

@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')

class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form) 

class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDetailView(LoginRequiredMixin, DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )

        return context


class BirthdayListView(LoginRequiredMixin, ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10



class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')



