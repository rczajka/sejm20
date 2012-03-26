# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from house.models import Glosowanie


class UserProfile(models.Model):
    user = models.OneToOneField(User, editable=False)
    description = models.CharField('krótki opis', max_length=255, null=True, blank=True, help_text='Czysty tekst.')
    url = models.URLField('strona internetowa', null=True, blank=True)

    @classmethod
    def for_user(cls, user):
        profile, created = cls.objects.get_or_create(user=user)
        return profile


class Vote(models.Model):
    glosowanie = models.ForeignKey(Glosowanie)
    user = models.ForeignKey(User)
    vote = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    vote_strings = {
        1: 'za',
        2: 'przeciw',
    }

    class Meta:
        unique_together = [['glosowanie', 'user']]
        ordering = ['-time']

    def __unicode__(self):
        return self.vote_strings[self.vote]


class Followship(models.Model):
    follower = models.ForeignKey(User, related_name='follows')
    followed = models.ForeignKey(User, related_name='followers')

    class Meta:
        unique_together = [['follower', 'followed']]
