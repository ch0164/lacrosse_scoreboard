from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from core.models import Roster, Coach
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login


# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()


            # Log the user in and redirect them to the home page.
            new_user = authenticate(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password1"])
            # Create and save a Coach object if the user is one.
            if form.cleaned_data["is_coach"]:
                coach = Coach(first_name=form.cleaned_data["first_name"],
                              last_name=form.cleaned_data["last_name"],
                              user=new_user)
                coach.save()
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserRegistrationForm()
        
    return render(request, "register.html", {"form": form})