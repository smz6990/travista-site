from django.shortcuts import render
from django.http import HttpResponse

def index_view(request):
    return  HttpResponse('<h1>Home page</h1>')

def about_view(request):
    return  HttpResponse('<h1>About page</h1>')

def contact_view(request):
    return  HttpResponse('<h1>Contact page</h1>')