from django.contrib import admin

from .models import Pokemon, PokemonEntity, PokemonElementType

admin.site.register((Pokemon, PokemonEntity, PokemonElementType))
