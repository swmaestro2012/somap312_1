# _*_ coding: utf-8 _*_
from models import Book, Branch, BookComment
from forms import BookCreationForm, BranchCreationForm, BookCommentForm

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def main_page(request):
    return render_to_response('index.html', RequestContext(request))


# 명예의전당
@login_required(login_url='/accounts/login/')
def recommend_list(request):
    # TODO: Ajax for pagenation
    book_list = Book.objects.all().exclude(root_branch=0)
    return render_to_response('posts/recommend_list.html', RequestContext(request, {
            'email': request.user,
            'book_list': book_list,
        }))


# 최신작
@login_required(login_url='/accounts/login/')
def show_newlist(request):
    # TODO: Ajax for pagenation
    book_list = Book.objects.all().exclude(root_branch=0)
    return render_to_response('posts/recommend_list.html', RequestContext(request, {
            'email': request.user,
            'book_list': book_list,
        }))


# 책갈피



# 심은 책
@login_required(login_url='/accounts/login/')
def show_mywork(request):
    mywork = Book.objects.all().filter(creator=request.user)
    return render_to_response('posts/show_mywork.html', RequestContext(request, {
            'book_list': mywork,
        }))


# 붙인가지


# 댓글 한 잎


# 책심기
@login_required(login_url='/accounts/login/')
def create_book(request):
    if request.method == "POST":
        book_form = BookCreationForm(request.POST, request.FILES)
        print book_form.errors
        if book_form.is_valid():
            book_form.save()
            return HttpResponseRedirect('/')

    book_form = BookCreationForm({ 'creator': request.user })
    
    return render_to_response('posts/create_book.html', \
        RequestContext(request, { 'form': book_form } ))


# 작성중인 가지


# 관심작가


# 계정 설정


# 고객센터


####################


## 책 정보
@login_required(login_url='/accounts/login/')
def get_bookinfo(request, book_id):
# fields = ('book', 'writer', 'text',)
    # TODO: ajax
    if request.method == "POST":
        bookcomment_form = BookCommentForm(request.POST)
        print bookcomment_form.errors
        if bookcomment_form.is_valid():
            bookcomment_form.save()
            return HttpResponseRedirect('/posts/get_bookinfo/' + book_id)

    
    book_info = Book.objects.get(id=book_id)
    branch_list = Branch.objects.filter(book=book_id)
    bookcoment = BookComment.objects.all().filter(book=book_id)


    bookcomment_form = BookCommentForm({'book': book_info,
                                        'writer' : request.user})

    return render_to_response("posts/get_bookinfo.html", RequestContext(request, {
            "book_info": book_info,
            "branch_list": branch_list,

            "bookcomment_form": bookcomment_form,
            "bookcomments": bookcoment,
    }))


## About 가지
@login_required(login_url='/accounts/login/')
def write_branch(request, book_info, parent_branch):
# fields = ('book', 'title', 'author', 'contents', 'parent_branch',)

    if request.method == "POST":
        branch_form = BranchCreationForm(request.POST)    
        print branch_form.errors
        if branch_form.is_valid():            
            branch = branch_form.save()

            # Update Book of root_branch            
            book = Book.objects.get(pk=book_info)
            book.root_branch = branch
            book.save()
            
            return HttpResponseRedirect('/')

    # if no branch in the book, send 0
    branch_form = BranchCreationForm({'author': request.user,
                                      'book': book_info,
                                      'parent_branch': parent_branch})
    # Will Post parent_branch_id, Book_id
    return render_to_response('posts/write_branch.html', \
        RequestContext(request, {'form': branch_form,
                                 'book_info': book_info,
                                 'parent_branch': parent_branch } ))


@login_required(login_url='/accounts/login/')
def read_branch(request, branch_id):
    if request.method == "GET":
        
        branch = Branch.objects.get(pk=branch_id)
        # Page Not found if don't have branch id
        
        return render_to_response('posts/read_branch.html', \
            RequestContext(request, {'branch': branch,
                                     }))
    # Page Not found    
    return HttpResponseRedirect('/')