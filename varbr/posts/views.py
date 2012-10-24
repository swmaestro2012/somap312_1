from forms import BookCreationForm

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def create_book(request):
    if request.method == "POST":
        book_form = BookCreationForm(request.POST, request.FILES)
        print book_form.errors
        if book_form.is_valid():
            book_form.save()
            return HttpResponseRedirect('/')

    book_form = BookCreationForm({ 'creator': 1 })

    return render_to_response('posts/create_book.html', \
        RequestContext(request, { 'form': book_form } ))
