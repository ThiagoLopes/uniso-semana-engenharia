from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from .models import Palestra, Palestrante, Registred
from .forms import RegistredForms


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_qs_palestrante(self):
        speaker_four = Palestrante.objects.filter(show_home=True)[:6]
        return speaker_four

    def get_qs_palestra(self):
        return Palestra.objects.all().prefetch_related('palestrante')

    def get_qs_all_days_distinct(self):
        all_days = Palestra.objects.dates('date', 'day')
        return all_days

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['palestra_list'] = self.get_qs_palestra()
        context['palestrante_list'] = self.get_qs_palestrante()
        context['all_days'] = self.get_qs_all_days_distinct()
        return context


home_template_view = HomeTemplateView.as_view()


class RegistredFormView(SuccessMessageMixin, CreateView):
    template_name = 'registred_new.html'
    form_class = RegistredForms
    success_url = '/'
    model = Registred
    success_message = _('Inscrição concluida com sucesso')

    def get(self, *args, **kwargs):
        context = super().get(*args, **kwargs)
        return context


registred_form_view = RegistredFormView.as_view()
