from django.views.generic.base import TemplateView
from .models import Palestra, Palestrante


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_qs_palestrante(self):
        speaker_four = Palestrante.objects.all()[:6]
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
