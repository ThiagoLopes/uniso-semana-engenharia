from django.contrib import admin
from .models import Palestra, Palestrante

# Register your models here.


class PalestraAdmin(admin.ModelAdmin):
    empty_value_display = '-vazio-'


class PalestranteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Palestra, PalestraAdmin)
admin.site.register(Palestrante, PalestranteAdmin)
