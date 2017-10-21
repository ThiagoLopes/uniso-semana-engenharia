from django.contrib import admin
from .models import Palestra

# Register your models here.


class PalestraAdmin(admin.ModelAdmin):
    empty_value_display = '-vazio-'


admin.site.register(Palestra, PalestraAdmin)
