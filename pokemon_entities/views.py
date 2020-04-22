import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon.entities.all():
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.long,
                pokemon.title, request.build_absolute_uri(pokemon.image.url))

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': (pokemon.image and pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def prepare_view_description(pokemon: Pokemon) -> dict:
    information = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": pokemon.image.url,
    }

    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        information['next_evolution'] = {
            "title_ru": next_evolution.title,
            "pokemon_id": next_evolution.id,
            "img_url": next_evolution.image.url
        }

    if pokemon.previous_evolution:
        information['previous_evolution'] = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": pokemon.previous_evolution.image.url
        }

    information['element_type'] = [{'title': element_type.title,
                                    'img': element_type.image.url,
                                    'strong_against': element_type.strong_against.all()
                                    } for element_type in
                                   pokemon.elements.all()]

    return information


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.filter(pk=pokemon_id).first()

    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_description = prepare_view_description(pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.entities.all():
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.long,
            pokemon.title, request.build_absolute_uri(pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_description})
