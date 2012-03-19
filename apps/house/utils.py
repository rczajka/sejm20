"""
General utilities.
"""
import re
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ModelFromApi(models.Model):
    class Meta:
        abstract = True

    @staticmethod
    def related_getter(model):
        def wrapped(api_obj):
            pk = getattr(api_obj.info, "%s_id" % model.__name__.lower())
            try:
                return model._default_manager.get(pk=pk)
            except model.DoesNotExist:
                return None
        return wrapped

    @classmethod
    def update(cls, verbose=True, only_new=False):
        import sejmometr
        for api_obj in getattr(sejmometr, cls.__name__).lista():
            try:
                obj = cls._default_manager.get(pk=api_obj.id)
            except cls.DoesNotExist:
                obj = cls()
                created = True
            else:
                created = False

            if only_new and not created:
                continue

            if verbose:
                print "%s %d" % (cls.__name__, api_obj.id)

            fields, cfields = cls.update_fields()
            data = {}
            rel_data = {}
            for arg in fields:
                data[arg] = getattr(api_obj.info, arg)
            for k, v in cfields.items():
                value = v(api_obj)
                data[k] = v(api_obj)

            after_save = []
            for k, v in data.items():
                # Some fields must wait for saving.
                if created:
                    try:
                        getattr(obj, k)
                    except ValueError:
                        # It's a relation, leave it till after save.
                        after_save.append(k)
                        continue
                    except ObjectDoesNotExist:
                        # It's just a ForeignKey, it's ok.
                        pass
                setattr(obj, k, v)
            obj.save()
            if after_save:
                for k in after_save:
                    setattr(obj, k, data[k])
                obj.save()


def str2int(string):
    nr = re.match(r'\d*', string).group()
    return int(nr) if nr != '' else 0
