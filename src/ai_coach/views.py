from django.shortcuts import render



def home_view(request):
    return render(request, "home.html")

def signin(request):
    return render(request, "signin.html")

def signup(request):
    return render(request, "signup.html")

def survey(request):
    return render(request, "survey.html")