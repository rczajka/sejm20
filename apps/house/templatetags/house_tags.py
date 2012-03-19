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

@register.inclusion_tag("house/snippets/punkt_link.html")
def punkt_link(punkt, more=None):
    return {'obj': punkt,
            'more': more,
            'users': people.api.users_for_punkt(punkt),
            }

@register.inclusion_tag("house/snippets/glosowanie_link.html")
def glosowanie_link(glosowanie, more=None):
    return {'obj': glosowanie,
            'more': more,
            'users': people.api.users_for_glosowanie(glosowanie),
            }

@register.inclusion_tag("house/snippets/glosowanie_link_short.html")
def glosowanie_link_short(glosowanie, more=None):
    return glosowanie_link(glosowanie, more)


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
