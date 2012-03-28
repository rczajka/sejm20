from django import template
import people.api
register = template.Library()


@register.inclusion_tag("house/snippets/klub_link.html")
def klub_link(klub, more=None):
    return {'obj': klub,
            'more': more,
            }

@register.inclusion_tag("house/snippets/druk_link.html")
def druk_link(druk, more=None):
    return {'obj': druk,
            'more': more,
            }

@register.inclusion_tag("house/snippets/posiedzenie_link.html")
def posiedzenie_link(posiedzenie, more=None):
    return {'obj': posiedzenie,
            'more': more,
            'users': people.api.users_for_posiedzenie(posiedzenie),
            }

@register.inclusion_tag("house/snippets/punkt_list.html")
def punkt_list(punkty):
    for p in punkty:
        p.users = people.api.users_for_punkt(p)
    return {'punkty': punkty}

@register.inclusion_tag("house/snippets/glosowanie_list.html", takes_context=True)
def glosowanie_list(context, glosowania):
    return {
            'request': context['request'],
            'glosowania': glosowania
            }

@register.inclusion_tag("house/snippets/glosowanie_link.html", takes_context=True)
def glosowanie_link(context, glosowanie, user=None):
    request = context['request']
    if user is None:
        user = user or request.user
    return {
            "obj": glosowanie,
            "vote": people.api.get_vote(user, glosowanie),
            "users": people.api.users_for_glosowanie(glosowanie),
        }

@register.inclusion_tag("house/snippets/posel_link.html")
def posel_link(posel, rating=None):
    return {
        'obj': posel,
        'rating': rating,
    }


@register.inclusion_tag("house/snippets/klub_link.html")
def klub_link(klub, rating=None):
    return {
        'obj': klub,
        'rating': rating,
    }
