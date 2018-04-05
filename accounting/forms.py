from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25,widget=forms.TextInput
            (attrs={
                    "class": "custom-class",
                    "placeholder": "Preencha seu nome"}))
    #email = forms.EmailField()
    message = forms.CharField(max_length=250,widget=forms.Textarea
            (attrs={
                    "class": "custom-class",
                    "placeholder": "Insira uma mensagem ao seu destinatario, o Balanço será enviado aos remetentes abaixo inseridos"}))
    to = forms.EmailField(help_text='A valid email address, please.')
    cc = forms.EmailField(help_text='Insert another e-mail here if necessary',required=False)
    #attach = forms.Field(widget = forms.FileInput)
    #comments = forms.CharField(required=False, widget=forms.Textarea)
