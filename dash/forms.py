# coding: utf-8

import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from .models import Registred, Palestra


class PalestraChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return _('{} / Dia {}, das {} às {}').format(
           str(obj),
           obj.date.day,
           obj.hour_init.strftime('%H:%M'),
           obj.hour_end.strftime('%H:%H')
        )


class RegistredForms(forms.ModelForm):

    error_messages = {
        'invalid': _('CPF invalido.'),
        'max_digits': _('Esse campo precisa ter de 11~14'),
        'digits_only': _('Apenas numeros'),
        'age_invalid': _('Idade não pode ser negativa ou 0'),
        'age_not_allow': _('Apenas maiores de 16')
    }

    palestra = PalestraChoiceField(
        label=_('Cursos'),
        help_text=_('Apenas cursos necessitam de inscrição'),
        queryset=Palestra.objects.filter(type=Palestra.COURSE),
        widget=forms.CheckboxSelectMultiple)

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('document')
        # verifica se cpf é valido
        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        try:
            int(value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])
        if len(value) != 11:
            raise ValidationError(self.error_messages['max_digits'])
        orig_dv = value[-2:]
        new_1dv = sum([i * int(value[idx])
                       for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx])
                       for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])
        # verifica idade

        idade = cleaned_data.get('age')
        if idade <= 0:
            raise ValidationError(self.error_messages.get('age_invalid'))

        if idade < 16:
            raise ValidationError(self.error_messages.get('age_not_allow'))

    class Meta:
        model = Registred
        fields = '__all__'


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0
