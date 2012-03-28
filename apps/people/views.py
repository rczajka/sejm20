# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from house.models import Glosowanie, Klub, Posel
from people import api
from django.core.urlresolvers import reverse
from people.forms import UserProfileForm, UserDeleteForm
from people.models import UserProfile, Vote
from django.contrib.auth import logout


def retain_POST(view):
    def wrapped(request, *args, **kwargs):
        if request.method == 'GET' and '_old_post' in request.session:
            request.POST = request.session['_old_post']
            request.method = 'POST'
            del request.session['_old_post']
        response = view(request, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect):
            request.session['_old_post'] = request.POST
        return response
    return wrapped


@retain_POST
@login_required
@require_POST
def vote(request, pk):
    glosowanie = get_object_or_404(Glosowanie, pk=pk)
    glos = request.POST.get('vote') # FIXME: should be a form
    api.vote(request.user, glosowanie, glos)
    return HttpResponseRedirect(glosowanie.get_absolute_url())

@retain_POST
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


@retain_POST
@login_required
@require_POST
def follow(request, username):
    user = get_object_or_404(User, username=username)
    api.follow(request.user, user)
    return HttpResponseRedirect(reverse("people_user", args=[username]))


@retain_POST
@login_required
@require_POST
def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    api.unfollow(request.user, user)
    return HttpResponseRedirect(reverse("people_user", args=[username]))


@login_required
def settings(request):
    profile = UserProfile.for_user(request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()

    else:
        form = UserProfileForm(instance=profile)
    return render(request, "people/settings.html", locals())


def user(request, username):
    user = get_object_or_404(User, username=username)
    follows = api.followed(user)
    followers = api.followers(user)
    return render(request, "people/user.html", locals())


def users(request):
    users = User.objects.all().annotate(c=Count('vote')).order_by('-c')
    return render(request, "people/users.html", locals())


@login_required
def user_delete(request):
    if request.method == 'POST':
        form = UserDeleteForm(request.user, data=request.POST)
        if form.is_valid():
            request.user.delete()
            logout(request)
            return render(request, "people/user_deleted.html")
    else:
        form = UserDeleteForm(request.user)
    return render(request, "people/user_delete.html", locals())
