from django.shortcuts import render


def index(request):
    return render(request, "nameless/index.html", {"title": "Nameless"})
