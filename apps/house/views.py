from django.shortcuts import get_object_or_404, render
from django.db.models import Count

from house.models import Posel, Glosowanie, Posiedzenie, Punkt, Klub
import people.api
from people.models import Vote


def klub(request, slug):
    klub = get_object_or_404(Klub, skrot=slug)
    deputys = people.api.rank_in_club(request.user, klub)
    rating = people.api.rate_club(request.user, klub)
    return render(request, "house/klub_detail.html", locals())


def posel(request, slug):
    posel = get_object_or_404(Posel, slug=slug)
    rating = people.api.rate(request.user, posel)
    return render(request, "house/posel_detail.html", locals())


def posiedzenia(request):
    posiedzenia = Posiedzenie.objects.all()
    return render(request, "house/posiedzenie_list.html", locals())


def posiedzenie(request, pk):
    posiedzenie = get_object_or_404(Posiedzenie, pk=pk)
    punkty = posiedzenie.punkt_set.all()
    glosowania = posiedzenie.glosowanie_set.filter(punkt=None)
    return render(request, "house/posiedzenie_detail.html", locals())


def punkt(request, pk):
    punkt = get_object_or_404(Punkt, pk=pk)
    glosowania = punkt.glosowanie_set.all()
    return render(request, "house/punkt_detail.html", locals())


def glosowanie(request, pk):
    glosowanie = get_object_or_404(Glosowanie, pk=pk)
    my_vote = people.api.get_vote(request.user, glosowanie)
    return render(request, "house/glosowanie_detail.html", locals())


def glosowania(request):
    glosowania = Glosowanie.objects.all().annotate(c=Count('vote')).order_by('-c', '-time')
    return render(request, "house/glosowania.html", locals())
