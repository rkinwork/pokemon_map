from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField('Наименование', max_length=200)
    image = models.ImageField('Изображение', blank=True)
    strong_against = models.ManyToManyField("self",
                                            verbose_name="Силён против",
                                            related_name='weak_from',
                                            symmetrical=False,
                                            blank=True
                                            )

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    title = models.CharField('Наименование', max_length=200)
    title_en = models.CharField('Английское наименование', max_length=200, blank=True)
    title_jp = models.CharField('Японское наименование', max_length=200, blank=True)
    image = models.ImageField('Изображение', blank=True)
    description = models.TextField('Описание', blank=True)
    previous_evolution = models.ForeignKey('self',
                                           models.SET_NULL,
                                           related_name='next_evolutions',
                                           verbose_name='Из кого эволюционировал',
                                           blank=True,
                                           null=True)
    elements = models.ManyToManyField(PokemonElementType,
                                      related_name='pokemons',
                                      verbose_name='Стихии',
                                      blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', related_name='entities', on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    long = models.FloatField('Долгота')
    appeared_at = models.DateTimeField("Появится в", null=True, blank=True)
    disappeared_at = models.DateTimeField("Исчезнет в", null=True, blank=True)
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return f"lat {self.lat} lon: {self.long}"
