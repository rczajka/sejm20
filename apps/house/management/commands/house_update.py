# -*- coding: utf-8 -*-
# This file is part of Sejm20, licensed under GNU Affero GPLv3 or later.
# Copyright 2011 Radek Czajka. See NOTICE for more information.
#
from django.core.management.base import BaseCommand

from house.helpers import update


class Command(BaseCommand):
    help = 'Updates data from sejmometr.'

    def handle(self, *args, **options):
        update()

