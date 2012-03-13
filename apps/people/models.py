from django.contrib.auth.models import User
from django.db import models

from house.models import Glosowanie


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

    def vote_string(self):
        return self.vote_strings[self.vote]


class Followship(models.Model):
    follower = models.ForeignKey(User, related_name='follows')
    followed = models.ForeignKey(User, related_name='followers')

    class Meta:
        unique_together = [['follower', 'followed']]
