# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField


class ModelFromApi(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def self_update(cls):
        print cls.fields


class Klub(ModelFromApi):
    nazwa = models.CharField(max_length=128)
    skrot = models.CharField(max_length=16)

    @models.permalink
    def get_absolute_url(self):
        return ('house_klub', [self.pk])

    def __unicode__(self):
        return self.nazwa

    @classmethod
    def update(cls):
        import sejmometr
        for api_obj in sejmometr.Klub.lista():
            data = {"nazwa": api_obj.info.nazwa,
                    "skrot": api_obj.info.skrot,
                    }
            obj, creat = cls.objects.get_or_create(pk=api_obj.id, defaults=data)
            if not creat:
                cls.objects.filter(pk=obj.id).update(**data)


class Posel(ModelFromApi):
    slug = models.SlugField(unique=True)
    imie = models.CharField(max_length=128)
    nazwisko = models.CharField(max_length=128)
    klub = models.ForeignKey(Klub, null=True, blank=True)

    class Meta:
        ordering = ['nazwisko', 'imie']

    def __unicode__(self):
        return "%s %s" % (self.imie, self.nazwisko)

    def sejmometr_url(self):
        return "http://sejmometr.pl/%s" % self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('house_posel', [self.slug])

    @classmethod
    def update(cls):
        import sejmometr
        for api_obj in sejmometr.Posel.lista():
            try:
                klub = Klub.objects.get(pk=api_obj.info.klub_id)
            except Klub.DoesNotExist:
                klub = None
            data = {"slug": api_obj.info.slug,
                    "imie": api_obj.info.imie,
                    "nazwisko": api_obj.info.nazwisko,
                    "klub": klub,
                    }
            obj, creat = cls.objects.get_or_create(pk=api_obj.id, defaults=data)
            if not creat:
                cls.objects.filter(pk=obj.id).update(**data)


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

    @classmethod
    def update(cls):
        import sejmometr
        for api_obj in sejmometr.Posiedzenie.lista():
            data = {"tytul": api_obj.info.tytul,
                    "data_start": api_obj.info.data_start,
                    "data_stop": api_obj.info.data_stop,
                    "ilosc_glosowan": api_obj.info.ilosc_glosowan,
                    }
            obj, creat = cls.objects.get_or_create(pk=api_obj.id, defaults=data)
            if not creat:
                cls.objects.filter(pk=obj.id).update(**data)


class Punkt(ModelFromApi):
    posiedzenie = models.ForeignKey(Posiedzenie)
    nr = models.CharField(max_length=64)
    nr_int = models.IntegerField()
    tytul = models.TextField()

    class Meta:
        ordering = ['posiedzenie', 'nr']

    def __unicode__(self):
        return u"Punkt %s: %s (%d głos.)" % (self.nr, self.tytul, self.glosowanie_set.count())

    @models.permalink
    def get_absolute_url(self):
        return ('house_punkt', [self.pk])

    @classmethod
    def update(cls):
        import re
        import sejmometr

        for api_obj in sejmometr.Punkt.lista():
            posiedzenie = Posiedzenie.objects.get(pk=api_obj.info.posiedzenie_id)
            nr = re.match(r'\d*', api_obj.info.nr).group()
            nr = int(nr) if nr != '' else 0
            data = {"posiedzenie": posiedzenie,
                    "nr": api_obj.info.nr,
                    "nr_int": nr,
                    "tytul": api_obj.info.tytul,
                    }
            obj, creat = cls.objects.get_or_create(pk=api_obj.id, defaults=data)
            if not creat:
                cls.objects.filter(pk=obj.id).update(**data)


class Glosowanie(ModelFromApi):
    posiedzenie = models.ForeignKey(Posiedzenie)
    punkt = models.ForeignKey(Punkt, null=True, blank=True)
    nr = models.IntegerField()
    tytul = models.TextField()
    time = models.DateTimeField()
    wyniki = JSONField(default=[])

    class Meta:
        ordering = ['time']

    def sejmometr_url(self):
        return "http://sejmometr.pl/glosowanie/%d" % self.pk

    @models.permalink
    def get_absolute_url(self):
        return ('house_glosowanie', [self.pk])

    @classmethod
    def update(cls):
        import sejmometr
        for api_obj in sejmometr.Glosowanie.lista():
            punkt = Punkt.objects.get(pk=api_obj.info.punkt_id) if api_obj.info.punkt_id else None
            posiedzenie = Posiedzenie.objects.get(pk=api_obj.info.posiedzenie_id)
            wyniki = [(int(w.posel.id), int(w.klub.id), int(w.glos)) for w in api_obj.wyniki]
            data = {"posiedzenie": posiedzenie,
                    "punkt": punkt,
                    "nr": api_obj.info.nr,
                    "tytul": api_obj.info.tytul,
                    "time": api_obj.info.time,
                    "wyniki": wyniki,
            }
            obj, creat = cls.objects.get_or_create(pk=api_obj.id, defaults=data)
            if not creat:
                cls.objects.filter(pk=obj.id).update(**data)
