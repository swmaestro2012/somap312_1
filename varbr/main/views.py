# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

@login_required(login_url='/accounts/login/')
def main_page(request):
    return render_to_response('main/main.html', RequestContext(request, {
            'email': request.user,
        }))

