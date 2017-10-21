from django.views.generic.base import TemplateView
from .models import Palestra

# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def qs_palestra(self):
        speaker_four = Palestra.objects.all()[:8]
        return speaker_four

    def get_qs_all_days_distinct(self):
        all_days = Palestra.objects.dates('date', 'day')
        return all_days

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['palestra_list'] = self.qs_palestra()
        context['all_days'] = self.get_qs_all_days_distinct()
        return context


home = HomeTemplateView.as_view()
