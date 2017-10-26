from django.contrib import admin
from .models import Palestra, Palestrante

# Register your models here.


class PalestraAdmin(admin.ModelAdmin):
    list_display = ('talk_name', 'talk_description', 'local', 'hour_init',
                    'hour_end', 'palestrantes')
    filter_horizontal = ('palestrante',)

    def palestrantes(self, obj):
        return ', '.join([str(p) for p in obj.palestrante.all()])


class PalestranteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Palestra, PalestraAdmin)
admin.site.register(Palestrante, PalestranteAdmin)
