from django import template
import people.api
register = template.Library()


def inclusion_tag(name):
    f = lambda o: {'obj': o}
    f.__name__ = name
    return f

for t in 'glosowanie', 'klub', 'posiedzenie', 'punkt':
    register.inclusion_tag('house/snippets/%s_link.html' % t
                           )(inclusion_tag("%s_link" % t))


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
