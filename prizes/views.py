from django import forms
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.shortcuts import render, redirect, HttpResponse
from django.utils.timezone import now
from uuid import uuid4
import hmac
import hashlib
import sys
from django.conf import settings
from models import Winner


def get_key(request):
    u4 = uuid4()
    return HttpResponse(u4.hex, mimetype="text/plain")


class PrizesError(PermissionDenied):
    pass


def check_key(request):
    key = request.REQUEST.get("key")
    sign = request.REQUEST.get("sign")

    if key is None or sign is None:
        raise PrizesError("There seems to be a bunch of information missing from that URL. "
                          "You're not supposed to visit it directly, you know.")

    cc = request.REQUEST.get("cc")
    h1 = hmac.new(settings.PRIZES_SECRET_KEY, key, hashlib.sha1)
    if h1.hexdigest() != sign:
        raise PrizesError("The signature is invalid for the key you supplied. "
                          "Are you up to... shenanigans?")
    winner, created = Winner.objects.get_or_create(key=key, defaults={'creation_ip': request.META.get("REMOTE_ADDR")})
    winner.authentication_time = now()
    winner.save()

    if cc == "yep":
        if request.session.test_cookie_worked():
            request.session['authenticated_winner'] = winner.id
            request.session.delete_test_cookie()
            return redirect(enter_details)
        else:
            return render(request, "prizes/no_cookies.html", {"key": key, "sign": sign})
    else:
        request.session.set_test_cookie()
        qd = QueryDict('', mutable=True)
        qd.update({"key": key, "sign": sign, "cc": "yep"})
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
    address1 = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}))
    address2 = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"size": "40"}))
    city = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}))
    state = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"size": "40"}))
    postcode = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"size": "40"}))
    country = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"size": "40"}))

    class Meta:
        model = Winner
        fields = []


def enter_details(request):
    winner = get_winner(request)
    if request.method == "POST":
        form = WinnerForm(request.POST, instance=winner)
        if form.is_valid():
            winner = form.save(commit=False)
            winner.details_time = now()
            winner.save()
            return redirect(thanks)
    else:
        form = WinnerForm(instance=winner)

    return render(request, "prizes/enter_details.html", {"form": form, "winner": winner})


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


def guru_error(request):
    raise Exception("Testing Guru Error")