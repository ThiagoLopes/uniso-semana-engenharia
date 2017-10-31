from django.db import models
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField,
                                         AutoSlugField)

# Create your models here.


class Palestrante(models.Model):

    speaker_name = models.CharField(_('Nome do palestrante'), max_length=45)
    speaker_description = models.TextField(
        _('Sobre o palestrante'), max_length=120, null=True)
    image = models.ImageField(upload_to='palestrante/%Y',
                              default='speaker-1.png')
    show_home = models.BooleanField(_('Mostrar na pagina inicial?'),
                                    default=False, blank=True)

    def __str__(self):
        return self.speaker_name

    def crop_values(self, width, height):
        new_height, new_width = [min(width, height)] * 2
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2
        return (left, top, right, bottom)

    def crop_image(self, original):
        image = Image.open(original)
        image_cropped = image.crop(self.crop_values(original.width,
                                                    original.height))
        image_cropped.save(original.file.name, image_cropped.format)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image.name != 'speaker-1.png':
            self.crop_image(self.image)

    class Meta:
        verbose_name = _('Palestrante cadastrado')
        verbose_name_plural = _('Palestrantes cadastrados')


class Palestra(models.Model):

    MEETUP = 1
    COURSE = 2
    SHOWCASE = 3
    PRESENTATION = 4

    TYPE = (
        (MEETUP, _('Meetup')),
        (COURSE, _('Curso')),
        (SHOWCASE, _('Demonstração')),
        (PRESENTATION, _('Apresentação'))
    )

    talk_name = models.CharField(
        _('Nome da palestra'), max_length=45, unique=True)
    talk_description = models.TextField(
        _('Descrição da palestra'), max_length=90)
    local = models.CharField(
        _('Prédio/Bloco da palestra'),
        help_text=_('Exemplo: Bloco X'), max_length=30)
    room = models.CharField(
        _('Sala da palestra'), max_length=30)
    date = models.DateField(
        _('Data'))
    hour_init = models.TimeField(
        _('Início'), help_text='HH/MM')
    hour_end = models.TimeField(
        _('Término'), help_text='HH/MM')
    number_vacancies = models.SmallIntegerField(
        _('Vagas'), default=100)
    created = CreationDateTimeField()
    modification = ModificationDateTimeField()
    slug = AutoSlugField(
        populate_from=['talk_name', 'room'])
    palestrante = models.ManyToManyField(Palestrante)
    type = models.SmallIntegerField(_('Formato'),
                                    choices=TYPE,
                                    default=PRESENTATION)

    @property
    def str_all_palestrante(self):
        return ', '.join([str(p) for p in self.palestrante.all()])

    @property
    def len_palestrantes(self):
        return len(self.palestrante.all())

    def __str__(self):
        return self.talk_name

    class Meta:
        verbose_name = _('Palestra cadastrada')
        verbose_name_plural = _('Palestras cadastrados')


class Registred(models.Model):

    name = models.CharField(_('Nome'), max_length=32)
    age = models.SmallIntegerField(_('Idade'))
    email = models.EmailField(_('Email'))
    palestra = models.ManyToManyField('Palestra')
    document = models.CharField(_('CPF'), max_length=14, unique=True)
    created = CreationDateTimeField()

    @property
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Estudante cadastrado')
        verbose_name_plural = _('Estudantes cadastrados')
