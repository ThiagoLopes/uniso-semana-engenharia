import datetime
from time import sleep
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase, Client
from .views import HomeTemplateView
from .models import Palestra

# Create your tests here.


class TestModel(TestCase):
    def setUp(self):
        t = datetime.datetime.now().time()
        self.data = {
            'talk_name': 'tester man',
            'talk_description': 'Lorem',
            'local': 'Brazil',
            'room': ' 10b',
            'date': datetime.date.today(),
            'hour_init': t,
            'hour_end': t.replace(hour=t.hour + 1),
            'number_vacancies': 100,
        }

    def test_model_palestra(self):
        p = Palestra.objects.create(**self.data)
        self.assertIsInstance(p, Palestra)

    def test_model_slugfield(self):
        p = Palestra.objects.create(**self.data)
        room = self.data.get('room').replace(' ', '-')
        talk_name = self.data.get('talk_name').replace(' ', '-')
        self.assertEqual(p.slug, '{}{}'.format(talk_name, room))

    def test_modification(self):
        p = Palestra.objects.create(**self.data)
        t = p.modification
        p.talk_name = 'tester man modification'
        sleep(.1)
        p.save()
        self.assertNotEqual(p.modification, t)


class TestHomeTemplateView(TestCase):
    def setUp(self):
        c = Client()
        page = reverse('dash:home')
        self.response = c.get(page)

    def test_home_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolve_view(self):
        page = resolve('/')
        self.assertEqual(page.func.view_class, HomeTemplateView)

    def test_as_context_palestra(self):
        self.assertIsNotNone(self.response.context.get('palestra_list'))

    def test_as_context_palestrante(self):
        self.assertIsNotNone(self.response.context.get('palestrante_list'))

    def test_as_context_all_days(self):
        self.assertIsNotNone(self.response.context.get('all_days'))
