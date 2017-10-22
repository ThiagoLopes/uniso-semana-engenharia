import os
import datetime
from time import sleep
from django.urls import resolve
from django.test import TestCase, Client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import HomeTemplateView
from .models import Palestra, Palestrante

# Create your tests here.


class TestModel(TestCase):
    def setUp(self):
        t = datetime.datetime.now().time()
        file_image = os.path.join(
            settings.STATICFILES_DIRS[0], 'img', 'logodae.png')
        image_mock = SimpleUploadedFile(
            name='test.png',
            content=open(file_image, 'rb').read(),
            content_type='image/png')
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
        self.data_palestrante = {
            'speaker_name': 'Man Speaker',
            'speaker_description': 'Lorem Lorem Lorem',
            'image': image_mock
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

    def test_model_palestrante(self):
        p = Palestrante.objects.create(**self.data_palestrante)
        self.assertIsInstance(p, Palestrante)

    def test_model_palestra_len_palestrante_one(self):
        palestrante = Palestrante.objects.create(**self.data_palestrante)
        palestra = Palestra.objects.create(**self.data)
        palestra.palestrante.add(palestrante)
        self.assertEqual(palestra.len_palestrantes, 1)

    def test_model_palestra_len_palestrante_two(self):
        palestrante_one = Palestrante.objects.create(**self.data_palestrante)
        palestrante_two = Palestrante.objects.create(**self.data_palestrante)
        palestra = Palestra.objects.create(**self.data)
        palestra.palestrante.add(palestrante_one)
        palestra.palestrante.add(palestrante_two)
        self.assertEqual(palestra.len_palestrantes, 2)

    def test_model_str_all_palestrante(self):
        palestrante = Palestrante.objects.create(**self.data_palestrante)
        palestra = Palestra.objects.create(**self.data)
        palestra.palestrante.add(palestrante)
        self.assertEqual(palestra.str_all_palestrante, str(palestrante))

    def test_property_len_palestra(self):
        p = Palestra.objects.create(**self.data)
        self.assertFalse(callable(p.len_palestrantes))

    def test_property_str_all_palestrante(self):
        p = Palestra.objects.create(**self.data)
        self.assertFalse(callable(p.str_all_palestrante))


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
