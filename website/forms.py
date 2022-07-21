from django import forms
from captcha.fields import CaptchaField

from website.models import Contact,Newsletter

class ContactForm(forms.ModelForm):
    
    captcha = CaptchaField()
    class Meta:
        model = Contact
        fields = '__all__'
        
        
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'