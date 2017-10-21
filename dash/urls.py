from django.conf.urls import url
from .views import home_template_view


urlpatterns = [
    url(r'^$', home_template_view, name='home')
]
