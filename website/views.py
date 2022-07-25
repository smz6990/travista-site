from django.shortcuts import render,redirect
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
            # new = form.save(commit=False)  # new.name = 'Anonymous'  # new.save()
            form.save()
            messages.success(request, 'Contact submitted successfully.')
        else :
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    # return  render(request,'website/contact.html')
    return redirect(reverse('website:contact'))
       
def newsletter_view(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter submitted successfully.')
        
        else :
            form = NewsletterForm()
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    if 'next' in request.POST:
        return redirect (request.POST.get('next','/'))
    return redirect('/')