from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

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

def index(request):
    return render_to_response('jQuery2.html')

