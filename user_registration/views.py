from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm
from core.models import Roster


# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # if form.fields["is_coach"] is True:
            #     name = form.cleaned_data["username"]
            #     roster = Roster(name=name)
            #     roster.save()
            #     request.user.roster.add(roster)

            form.save()
            return redirect("/")
    else:
        form = UserRegistrationForm()
        
    return render(request, "register.html", {"form": form})