from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import  messages
from website.forms import ContactForm,NewsletterForm


def index_view(request):
    return  render(request,'website/index.html')

def about_view(request):
    return  render(request,'website/about.html')

def contact_view(request):
    form = ContactForm()
    context = {
        'form':form,
    }
    return render(request,'website/contact.html',context)

def form_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
           
            # new = form.save(commit=False)
            # new.name = 'Anonymous'
            # new.save()
            form.save()
            
            messages.success(request, 'Contact submitted successfully.')
            # return  render(request,'website/contact.html')
            return HttpResponseRedirect(reverse('website:contact'))
        
        else :
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
            # return  render(request,'website/contact.html')
            return HttpResponseRedirect(reverse('website:contact'))
        
    else:
        # return  render(request,'website/contact.html')
        return HttpResponseRedirect(reverse('website:contact'))
    
    
def newsletter_view(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter submitted successfully.')
            return HttpResponseRedirect('/')
        
        else :
            form = NewsletterForm()
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')