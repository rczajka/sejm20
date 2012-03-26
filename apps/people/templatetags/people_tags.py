from django import template
from people.models import Vote
from people import api

register = template.Library()


@register.filter
def follows(user1, user2):
    return api.follows(user1, user2)


@register.inclusion_tag("people/snippets/users_list.html", takes_context=True)
def users_list(context, users):
    request = context['request']
    return {
            "request": request,
            "users": users,
        }


@register.inclusion_tag("people/snippets/user_link.html", takes_context=True)
def user_link(context, user):
    if not hasattr(user, 'c'):
        user.c = user.vote_set.count()
    return {"user": user}


@register.filter
def name(user):
    if user:
        return user.get_full_name() or user
    else:
        return ''


@register.inclusion_tag("people/snippets/rating.html")
def rating(rating):
    return {
        "rating": int(round(100 * rating)) if rating is not None else None,
        "no_rating": rating is None,
    }

@register.inclusion_tag("people/snippets/rating.html")
def rating_long(rating):
    return {
        "rating": int(round(100 * rating)) if rating is not None else None,
        "no_rating": rating is None,
        "long": True,
    }

@register.filter
def percentage(rating):
    return "%.1f%%" % (100 * rating)

@register.inclusion_tag("people/snippets/voting_on.html")
def voting_on(glosowanie):
    users = ([], [])
    for v in glosowanie.vote_set.all():
        users[v.vote - 1].append(v.user)
    return {'users': users}


@register.inclusion_tag("people/snippets/users_inline.html")
def followers_inline(user, size=32):
    return {
        "users": (f.follower for f in user.followers.all()),
        "size": size,
    }

@register.inclusion_tag("people/snippets/user_glosowanie_list.html", takes_context=True)
def user_glosowanie_list(context, user):
    glosowania = [v.glosowanie for v in user.vote_set.all()]
    return {
            'glosowania': glosowania,
            'request': context['request'],
            }

@register.inclusion_tag("people/snippets/users_inline.html")
def users_inline(users, size=32):
    return locals()

@register.inclusion_tag("people/snippets/users_inline_links.html")
def users_inline_links(users, size=32):
    return locals()
