from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, User
from .models import Palestra, Palestrante, Registred

# Register your models here.


class PalestraAdmin(admin.ModelAdmin):
    list_display = ('talk_name', 'talk_description', 'local', 'hour_init',
                    'hour_end', 'palestrantes')
    filter_horizontal = ('palestrante',)

    def palestrantes(self, obj):
        return ', '.join([str(p) for p in obj.palestrante.all()])


class PalestranteAdmin(admin.ModelAdmin):
    list_display = ('speaker_name', 'speaker_description',
                    'show_home')


admin.site.site_header = _('Painel semana engenharia')
admin.site.site_title = _('Painel semana engenharia')
admin.site.index_title = _('Painel')
admin.site.register(Palestra, PalestraAdmin)
admin.site.register(Palestrante, PalestranteAdmin)
admin.site.register(Registred)
admin.site.unregister(Group)
admin.site.unregister(User)
