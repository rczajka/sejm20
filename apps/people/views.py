# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from house.models import Glosowanie
from people import api
from django.core.urlresolvers import reverse


@login_required
@require_POST
def vote(request, pk):
    glosowanie = get_object_or_404(Glosowanie, pk=pk)
    glos = request.POST.get('vote') # FIXME: should be a form
    api.vote(request.user, glosowanie, glos)
    return HttpResponseRedirect(glosowanie.get_absolute_url())

@login_required
@require_POST
def unvote(request, pk):
    glosowanie = get_object_or_404(Glosowanie, pk=pk)
    api.vote(request.user, glosowanie, None)
    return HttpResponseRedirect(glosowanie.get_absolute_url())


def rank(request):
    logged_in = request.user.is_authenticated()
    if logged_in:
        voted = request.user.vote_set.exists()
        follows = api.followed(request.user)
    deputys = api.rank(request.user)
    clubs = api.rank_clubs(request.user)
    return render(request, "people/rank.html", locals())


@login_required
@require_POST
def follow(request, username):
    user = get_object_or_404(User, username=username)
    api.follow(request.user, user)
    return HttpResponseRedirect(reverse("people_user", args=[username]))


@login_required
@require_POST
def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    api.unfollow(request.user, user)
    return HttpResponseRedirect(reverse("people_user", args=[username]))


@login_required
def my_page(request):
    user = request.user
    return render(request, "people/user.html", locals())


def user(request, username):
    user = get_object_or_404(User, username=username)
    follows = api.followed(user)
    followers = api.followers(user)
    return render(request, "people/user.html", locals())
