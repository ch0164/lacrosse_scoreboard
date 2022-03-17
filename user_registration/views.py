from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from core.models import Roster
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login


# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password1"])
            login(request, new_user)

            return HttpResponseRedirect("/")
    else:
        form = UserRegistrationForm()
        
    return render(request, "register.html", {"form": form})