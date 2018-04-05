from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.


def home(request):
    return render(request, 'accounting/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('accounting/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your #econobilidade account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'accounting/acc_active_sent.html')
            #return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'accounting/thankyou.html')
    else:
        return HttpResponse('Activation link is invalid!')



class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_Accounting(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Accounting],
                initializers=[None, choice_func],
                mapdicts=[
                    ['company','history', 'date', 'debit','credit','amount','conta_devedora','conta_credora']]
            )
            return render(request, 'accounting/thankyou2.html')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
            {
            'form': form,
            'title': 'Import excel data into database',
            'header': "Please upload your accounting Journal:"
        })




from django.core.mail.message import EmailMessage
#from django.contrib.auth.models import User
from .forms import EmailPostForm


@login_required
def email(request):
    if request.method == 'POST':
            form = EmailPostForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                email = EmailMessage()
                email.subject = "Your Balance Sheet just arrived"
                email.body = cd['message']
                email.to = [cd['to']]
                email.cc = [cd['cc']]
                email.attach_file("accounting/documents/Alzina - 04-04-2018 - 22-14.pdf") # Attach a file directly

                email.send()
                return render_to_response('accounting/thankyou2.html')

    else:
        form = EmailPostForm(request.POST)


    return render(request, 'accounting/share.html', context = {'form': form})



@login_required
def bs(request):
    return render(request, 'accounting/Balanço&DRE_2years_Hod.htm')
