# -*- coding: utf-8 -*-
'''
API for the people app. Views should only access models through here.

@author: Radek Czajka
'''
from collections import defaultdict
from house.models import Posel, Klub
from people.models import Vote, Followship
from django.db.models import Count, Max
from django.contrib.auth.models import User


def follow(user1, user2):
    assert user1.is_authenticated()
    assert user2.is_authenticated()
    Followship.objects.get_or_create(follower=user1, followed=user2)


def unfollow(user1, user2):
    assert user1.is_authenticated()
    assert user2.is_authenticated()
    Followship.objects.filter(follower=user1, followed=user2).delete()


def follows(user1, user2):
    if not user1.is_authenticated() or not user2.is_authenticated():
        return False
    return Followship.objects.filter(follower=user1, followed=user2).exists()


def vote(user, glosowanie, vote):
    assert user.is_authenticated()
    if vote is None:
        Vote.objects.filter(user=user, glosowanie=glosowanie).delete()
    else:
        v, c = Vote.objects.get_or_create(user=user, glosowanie=glosowanie, defaults={
            'vote': vote
        })
        if not c and v.vote != vote:
            v.vote = vote
            v.save()


def get_vote(user, glosowanie):
    if not user.is_authenticated():
        return None
    try:
        return glosowanie.vote_set.get(user=user)
    except Vote.DoesNotExist:
        return None


def rank(user, posel_ids=None):
    if posel_ids:
        poslowie = Posel.objects.in_bulk(posel_ids)
        poslowie = [poslowie[i] for i in posel_ids]
    else:
        poslowie = Posel.objects.all()

    if not user.is_authenticated():
        return [(p, None) for p in poslowie]

    totals = defaultdict(dict)
    goods = defaultdict(dict)
    my_votes = set()

    # first count my votes
    for vote in user.vote_set.all():
        my_votes.add(vote.id)
        for posel_id, klub_id, glos in vote.glosowanie.wyniki:
            if posel_ids and posel_id not in posel_ids:
                continue
            totals[posel_id][vote.id] = totals[posel_id].get(vote.id, 0) + 1
            if glos == vote.vote:
                goods[posel_id][vote.id] = goods[posel_id].get(vote.id, 0) + 1

    # count followed for followed people votes
    for flw in user.follows.all():
        for vote in flw.followed.vote_set.exclude(pk__in=my_votes):
            for posel_id, klub_id, glos in vote.glosowanie.wyniki:
                if posel_ids and posel_id not in posel_ids:
                    continue
                totals[posel_id][vote.id] = totals[posel_id].get(vote.id, 0) + 1
                if glos == vote.vote:
                    goods[posel_id][vote.id] = goods[posel_id].get(vote.id, 0) + 1

    ratings = []

    for p in poslowie:
        rating = 0
        for vote_id, total in totals[p.id].items():
            rating += float(goods[p.id].get(vote_id, 0)) / total
        final_rating = rating / len(totals[p.id]) if totals[p.id] else 0
        ratings.append((p, final_rating))

    return sorted(ratings, reverse=True, key=lambda x: x[1])


def rate(user, posel):
    if not user.is_authenticated():
        return None
    return rank(user, [posel.id])[0][1]


def rank_clubs(user):
    """Returks all the clubs, ranked by rating."""
    if not user.is_authenticated():
        return ((k, None) for k in Klub.objects.all().annotate(c=Count('posel')).order_by('-c'))

    clubs = defaultdict(list)
    for deputy, rating in rank(user):
        if deputy.klub is not None:
            clubs[deputy.klub.pk].append(rating)
    ratings = []
    for club in Klub.objects.all():
        if clubs.get(club.pk):
            rating = sum(clubs[club.pk]) / len(clubs[club.pk])
        else:
            rating = 0
        ratings.append((club, rating))
    return sorted(ratings, reverse=True, key=lambda x: x[1])


def rate_club(user, club):
    """Returns the rating of the club.
    
    It is calculated as the average rating of the current member of the club.
    """
    if not user.is_authenticated():
        return None
    if not club.posel_set.exists():
        return None
    return sum(x[1] for x in rank_in_club(user, club)) / club.posel_set.count()


def rank_in_club(user, club):
    """Returns all the deputys in the club, ranked by rating."""
    posel_ids = [p.id for p in club.posel_set.all()]
    return rank(user, posel_ids)


def users_for_posiedzenie(posiedzenie):
    users = (v.user for v in Vote.objects.filter(glosowanie__posiedzenie=posiedzenie))
    already = set()
    for u in users:
        if u.pk not in already:
            yield u
            already.add(u.pk)
def users_for_punkt(punkt):
    users = (v.user for v in Vote.objects.filter(glosowanie__punkt=punkt))
    already = set()
    for u in users:
        if u.pk not in already:
            yield u
            already.add(u.pk)
def users_for_glosowanie(glosowanie):
    return (v.user for v in glosowanie.vote_set.all())

def followers(user):
    return [f.follower for f in user.followers.all()]

def followed(user):
    return [f.followed for f in user.follows.all()]
