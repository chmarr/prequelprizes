# PrequelPrizes server-side code Copyright (c) 2013 Chris Cogdon - chris@cogdon.org

from uuid import uuid4
import hmac
import hashlib
import sys

from django import forms
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.shortcuts import render, redirect, HttpResponse
from django.utils.timezone import now
from django.conf import settings
from django.views.decorators.cache import never_cache, cache_control

from models import Winner


PRIZES_SECRET_KEY_STR = settings.PRIZES_SECRET_KEY.decode("hex")


@never_cache
def get_key(request):
    count = Winner.objects.exclude(details_time=None).values("authentication_ip").distinct().count()
    if count >= settings.PRIZES_NUM_PRIZES:
        return HttpResponse("0", mimetype="text/plain")
    else:
        u4 = uuid4()
        return HttpResponse(u4.hex, mimetype="text/plain")


class PrizesError(PermissionDenied):
    pass


@never_cache
def check_key(request):
    key = request.REQUEST.get("key")
    time = request.REQUEST.get("time")
    sign = request.REQUEST.get("sign")

    if key is None or sign is None or time is None:
        raise PrizesError("There seems to be a bunch of information missing from that URL. "
                          "You're not supposed to visit it directly, you know.")

    cc = request.REQUEST.get("cc")
    h1 = hmac.new(PRIZES_SECRET_KEY_STR, key + time, hashlib.sha1)
    if len(key) != 32 or h1.hexdigest() != sign:
        raise PrizesError("I'm pretty sure the game did not generate those numbers. "
                          "Are you up to... shenanigans?")

    try:
        game_time = float(time)
    except ValueError:
        raise PrizesError("That doesn't look like a valid game time. I think we messed up here.")

    try:
        winner = Winner.objects.get(key=key)
    except Winner.DoesNotExist:
        if settings.PRIZES_DISABLED:
            raise PrizesError("Somehow you managed to get the game to generate a prize link long after "
                              "all the prizes have been collected. Congratulations on doing that part, "
                              "but still no prize. Sorry.")
        winner = Winner(key=key, creation_ip=request.META.get("REMOTE_ADDR"))

    winner.authentication_time = now()
    winner.authentication_ip = request.META.get("REMOTE_ADDR")
    winner.game_time = game_time
    winner.save()

    if cc == "yep":
        if request.session.test_cookie_worked():
            request.session['authenticated_winner'] = winner.id
            request.session.delete_test_cookie()
            return redirect(enter_details)
        else:
            return render(request, "prizes/no_cookies.html", {"key": key, "time": time, "sign": sign})
    else:
        request.session.set_test_cookie()
        qd = QueryDict('', mutable=True)
        qd.update({"key": key, "time": time, "sign": sign, "cc": "yep"})
        return redirect(reverse(check_key) + "?" + qd.urlencode())


def get_winner(request):
    winner_id = request.session.get('authenticated_winner')
    if winner_id is None:
        raise PrizesError(
            "You have not been authenticated yet. "
            "Cookies blocked after I spent all that effort checking them for you? "
            "Bypassed the checkkey page by being sneaky?")
    try:
        winner = Winner.objects.get(id=winner_id)
    except Winner.DoesNotExist:
        raise PrizesError("The authenticated winner doesn't exist. How did you manage that? Amazing!")
    return winner


class WinnerForm(forms.ModelForm):
    email = forms.EmailField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}))
    name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}))
    address1 = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}), label="Address")
    address2 = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"size": "40"}), label="")
    city = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}))
    state = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"size": "40"}))
    postcode = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}), label="ZIP/Postcode")
    country = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"size": "40"}))

    class Meta:
        model = Winner
        fields = ["email", "name", "address1", "address2", "city", "state", "postcode", "country"]


@cache_control(private=True)
def enter_details(request):
    winner = get_winner(request)
    if request.method == "POST":
        form = WinnerForm(request.POST, instance=winner)
        if form.is_valid():
            winner = form.save(commit=False)
            winner.details_time = now()
            winner.details_ip = request.META.get("REMOTE_ADDR")
            winner.save()
            return redirect(thanks)
    else:
        form = WinnerForm(instance=winner)

    return render(request, "prizes/enter_details.html", {"form": form, "winner": winner})


@cache_control(private=True)
def thanks(request):
    try:
        winner = get_winner(request)
    except PrizesError:
        winner = None
    request.session.pop('authenticated_winner', None)
    return render(request, "prizes/thanks.html", {"winner": winner})


def handler403(request):
    exc_value = sys.exc_info()[1]
    exc_message = str(exc_value)
    return render(request, "403.html", {"exc_message": exc_message})
