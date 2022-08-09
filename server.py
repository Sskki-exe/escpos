
from email import contentmanager
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {
        "title": "your balls are mine"
    }
    return render(request, "index.html",context)