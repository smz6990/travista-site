from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserFrom(UserCreationForm):
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=255,required=False)
    last_name = forms.CharField(max_length=255,required=False)
    
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name','password1','password2')
    
    def save(self,commit=True):
        user = super(NewUserFrom, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if self.cleaned_data['first_name']:
            user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user    
        