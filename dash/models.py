from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField,
                                         AutoSlugField)

# Create your models here.


class Palestrante(models.Model):

    speaker_name = models.CharField(_('Nome do palestrante'), max_length=45)
    speaker_description = models.TextField(
        _('Sobre o palestrante'), max_length=45, null=True)
    image = models.ImageField(upload_to='palestrante/%Y',
                              null=False)

    def __str__(self):
        return self.speaker_name


class Palestra(models.Model):

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
        _('Início'))
    hour_end = models.TimeField(
        _('Término'))
    number_vacancies = models.SmallIntegerField(
        _('Vagas'))
    created = CreationDateTimeField()
    modification = ModificationDateTimeField()
    slug = AutoSlugField(
        populate_from=['talk_name', 'room'])
    palestrante = models.ManyToManyField(Palestrante)

    @property
    def str_all_palestrante(self):
        return ', '.join([str(p) for p in self.palestrante.all()])

    @property
    def len_palestrantes(self):
        return len(self.palestrante.all())

    def __str__(self):
        return self.talk_name
