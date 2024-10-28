from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
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


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related('author')
        )

        return context


class BirthdayListView(ListView):
    model = Birthday
    queryset = Birthday.objects.prefetch_related('tags').select_related('author')
    ordering = 'id'
    paginate_by = 10



class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')



# @login_required
# def add_comment(request, pk):
#     birthday = get_object_or_404(Birthday, pk=pk)
#     form = CongratulationForm(request.POST)

#     if form.is_valid():
#         congratulation = form.save(commit=False)
#         congratulation.author = request.user
#         congratulation.birthday = birthday
#         congratulation.save()
    
#     return redirect('birthday:detail', pk=pk)

class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # dispatch проверяет, что в базе есть объект дня рождения с переданными в запросе pk
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
        