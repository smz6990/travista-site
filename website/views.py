from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from website.forms import ContactForm,NewsletterForm


def index_view(request):
    return  render(request,'website/index.html')

def about_view(request):
    return  render(request,'website/about.html')


def contact_view(request):
    
    return  render(request,'website/contact.html')


def form_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('website:contact'))
        else :
            return HttpResponseRedirect(reverse('website:contact'))
    else:
        return HttpResponseRedirect(reverse('website:contact'))