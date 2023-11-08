from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'pottery/index.html')


def contact(request):
    return render(request, 'pottery/contact.html')


def default(request):
    return render(request, 'pottery/default.html')


def login(request):
    return render(request, 'pottery/login.html')


def register(request):
    return render(request, 'pottery/register.html')
