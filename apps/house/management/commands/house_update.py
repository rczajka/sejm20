# -*- coding: utf-8 -*-
# This file is part of Sejm20, licensed under GNU Affero GPLv3 or later.
# Copyright 2011 Radek Czajka. See NOTICE for more information.
#
from optparse import make_option
from django.core.management.base import BaseCommand

from house.helpers import update


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-q', '--quiet', action='store_false', dest='verbose', default=True,
            help='Suppress output'),
        make_option('-f', '--force-update', action='store_true', dest='force_update', default=False,
            help = "Force updating existing objects with new data."),
        )
    for letter, name in (('K', 'Klub'), ('P', 'Posel'), ('D', 'Druk'),
                        ('S', 'Posiedzenie'), ('T', 'Punkt'), ('G', 'Glosowanie')):
        option_list += (
            make_option('-%s' % letter,
                        '--no-%s' % name.lower(),
                        action = 'store_false',
                        dest = name,
                        default = True,
                        help = 'Update %s objects' % name
                        )
            , )
    help = 'Updates data from sejmometr.'

    def handle(self, *args, **options):
        update(**options)

