from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
"""
@csrf_exempt
def index(request):
    # TODO: Exception Handling
    # check username, email, password, duplicatied ...

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)

        print username + ' ' + email
        return HttpResponse(email)
    else:
        return HttpResponse('')i
"""
def signup_page(request):
    return render_to_response('accounts/signup.html', RequestContext(request, { 'form': UserCreationForm() }))

def redirect_to_login(request):
    return HttpResponseRedirect('/')

def signup_confirmed(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')

    signup_form = UserCreationForm(request.POST)

    if signup_form.is_valid():
        signup_form.clean_username()
        signup_form.clean_password2()
        signup_form.save()
    else:
        return render_to_response('accounts/signup.html', RequestContext(request, { 'form': signup_form, 'errors': signup_form.errors }))

    return HttpResponseRedirect('/')
