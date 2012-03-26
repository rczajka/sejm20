from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render

from house.models import Glosowanie, Posiedzenie


def home(request):
    posiedzenia = Posiedzenie.objects.all()[:6]
    glosowania = Glosowanie.objects.all().annotate(c=Count('vote')).order_by('-c', '-time')[:6]
    users = User.objects.all().annotate(c=Count('vote')).order_by('-c')[:8]

    return render(request, "home.html", locals())

