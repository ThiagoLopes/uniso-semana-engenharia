from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Palestra

# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    # TODO
    def qs_speakers(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        speakers_four = Palestra.objects.all()
        context['speaker_four_list'] = speakers_four
        return context


home = HomeTemplateView.as_view()
