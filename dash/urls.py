from django.conf.urls import url
from .views import home_template_view, registred_form_view


urlpatterns = [
    url(r'^$', home_template_view, name='home'),
    url(r'^new$', registred_form_view, name='registred')
]
