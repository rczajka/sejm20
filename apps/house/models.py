# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField
from house.utils import ModelFromApi, str2int


class Klub(ModelFromApi):
    nazwa = models.CharField(max_length=128)
    skrot = models.CharField(max_length=16, db_index=True)

    def __unicode__(self):
        return self.nazwa

    @models.permalink
    def get_absolute_url(self):
        return ('house_klub', [self.pk])

    def sejmometr_url(self):
        return "http://sejmometr.pl/%s" % self.skrot

    @classmethod
    def update_fields(cls):
        return ['nazwa', 'skrot'], {}


class Posel(ModelFromApi):
    slug = models.SlugField(unique=True, db_index=True)
    imie = models.CharField(max_length=128)
    nazwisko = models.CharField(max_length=128)
    klub = models.ForeignKey(Klub, null=True, blank=True)

    class Meta:
        ordering = ['nazwisko', 'imie']

    def __unicode__(self):
        return "%s %s" % (self.imie, self.nazwisko)

    @models.permalink
    def get_absolute_url(self):
        return ('house_posel', [self.slug])

    def sejmometr_url(self):
        return "http://sejmometr.pl/%s" % self.slug

    @classmethod
    def update_fields(cls):
        return (['slug', 'imie', 'nazwisko'],
                {'klub': lambda o: Klub.from_id(o.info.klub_id)})


class Druk(ModelFromApi):
    nr = models.CharField(max_length=32)
    nr_int = models.IntegerField(db_index=True)
    tytul = models.TextField()
    opis = models.TextField()
    dokument_id = models.IntegerField()

    class Meta:
        ordering = ['nr_int']

    def __unicode__(self):
        return u"Druk %s: %s" % (self.nr, self.tytul)

    def sejmometr_url(self):
        return "http://sejmometr.pl/druk/%s" % self.nr

    @classmethod
    def update_fields(cls):
        return (['nr', 'tytul', 'opis', 'dokument_id'],
                {'nr_int': lambda o: str2int(o.info.nr)})


class Posiedzenie(ModelFromApi):
    tytul = models.CharField(max_length=32)
    data_start = models.DateField(db_index=True)
    data_stop = models.DateField()
    ilosc_glosowan = models.IntegerField()

    class Meta:
        ordering = ['-data_start']

    def __unicode__(self):
        return u"Posiedzenie %s (%s — %s, %d głos.)" % (self.tytul, self.data_start, self.data_stop, self.ilosc_glosowan)

    @models.permalink
    def get_absolute_url(self):
        return ('house_posiedzenie', [self.pk])

    def sejmometr_url(self):
        return "http://sejmometr.pl/posiedzenia/%d" % self.pk

    @classmethod
    def update_fields(cls):
        return ['tytul', 'data_start', 'data_stop', 'ilosc_glosowan'], {}


class Punkt(ModelFromApi):
    posiedzenie = models.ForeignKey(Posiedzenie)
    nr = models.CharField(max_length=64)
    nr_int = models.IntegerField(db_index=True)
    tytul = models.TextField()
    druki = models.ManyToManyField(Druk)

    class Meta:
        ordering = ['posiedzenie', 'nr_int']

    def __unicode__(self):
        return u"Punkt %s: %s (%d głos.)" % (self.nr, self.tytul, self.glosowanie_set.count())

    @models.permalink
    def get_absolute_url(self):
        return ('house_punkt', [self.pk])

    def sejmometr_url(self):
        return "http://sejmometr.pl/punkt/%d" % self.pk

    @classmethod
    def update_fields(cls):
        def druki(api_obj):
            druki_ids = set([druk.id for druk in api_obj.druki])
            return [Druk.from_id(id) for id in druki_ids]
        return (['nr', 'tytul'],
                {'nr_int': lambda o: str2int(o.info.nr),
                 'posiedzenie': lambda o: Posiedzenie.from_id(o.info.posiedzenie_id),
                 'druki': druki})


class Glosowanie(ModelFromApi):
    posiedzenie = models.ForeignKey(Posiedzenie)
    punkt = models.ForeignKey(Punkt, null=True, blank=True)
    nr = models.IntegerField()
    tytul = models.TextField()
    time = models.DateTimeField(db_index=True)
    wyniki = JSONField(default=[])

    class Meta:
        ordering = ['time']

    def sejmometr_url(self):
        return "http://sejmometr.pl/glosowanie/%d" % self.pk

    @models.permalink
    def get_absolute_url(self):
        return ('house_glosowanie', [self.pk])

    @classmethod
    def update_fields(cls):
        def wyniki(api_obj):
            return [(int(w.posel.id), int(w.klub.id), int(w.glos))
                    for w in api_obj.wyniki]
        return (["nr", "tytul", "time"],
                {'posiedzenie': lambda o: (Posiedzenie.from_id(o.info.posiedzenie_id)),
                 'punkt': lambda o: (Punkt.from_id(o.info.punkt_id)),
                 'wyniki': wyniki})
