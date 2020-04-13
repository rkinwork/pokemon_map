from django.contrib import admin

from .models import Pokemon, PokemonEntity

admin.site.register((Pokemon, PokemonEntity))
