"""
Helper functions for the app's models.
"""

from house.models import Klub, Posel, Druk, Posiedzenie, Punkt, Glosowanie

def update(verbose=True, force_update=False, **kwargs):
    for cls in Klub, Posel, Druk, Posiedzenie, Punkt, Glosowanie:
        if kwargs and not kwargs.get(cls.__name__):
            continue
        if verbose:
            print "updating %s" % cls.__name__
        cls.update(verbose=verbose, force_update=force_update)
