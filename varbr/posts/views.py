# _*_ coding: utf-8 _*_
from models import Book, Branch, BookComment, BranchLike, Bookmark
from forms import BookCreationForm, BranchCreationForm, BookCommentForm

from django.http import HttpResponseRedirect, Http404
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
    book_list = Book.objects.all().exclude(root_branch=None)
    return render_to_response('posts/recommend_list.html', RequestContext(request, {
            'email': request.user,
            'book_list': book_list,
        }))


# 최신작
@login_required(login_url='/accounts/login/')
def show_newlist(request):
    # TODO: Ajax for pagenation
    book_list = Book.objects.all().exclude(root_branch=None)
    return render_to_response('posts/recommend_list.html', RequestContext(request, {
            'email': request.user,
            'book_list': book_list,
        }))


# 책갈피
def show_bookmarks(request):
    bookmark_list = Bookmark.objects.filter(user=request.user)

    return render_to_response('posts/working_branch.html', RequestContext(request, {
            'bookmark_list': bookmark_list,
        }))


# 심은 책
@login_required(login_url='/accounts/login/')
def show_mywork(request):
    mywork = Book.objects.all().filter(creator=request.user)
    return render_to_response('posts/show_mywork.html', RequestContext(request, {
            'book_list': mywork,
        }))


# 붙인 가지
def show_mybranches(request):
    branch_list_worked = Branch.objects.all().filter(author=request.user, is_temporary=False)
    return render_to_response('posts/working_branch.html', RequestContext(request, {
            'branch_list_worked': branch_list_worked,
        }))


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
@login_required(login_url='/accounts/login/')
def working_branch(request):
    # TODO: Ajax for pagenation
    branch_list = Branch.objects.all().filter(author=request.user, is_temporary=True)
    return render_to_response('posts/working_branch.html', RequestContext(request, {
            'branch_list': branch_list,
        }))


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
    

    for branch in branch_list:
        if branch.check_to_like(request.user):
            branch.is_liked = True

    bookcoment = BookComment.objects.all().filter(book=book_id)


    bookcomment_form = BookCommentForm({'book': book_info,
                                        'writer' : book_info.creator })

    return render_to_response("posts/get_bookinfo.html", RequestContext(request, {
            "user": request.user.id,
            "book_info": book_info,
            "branch_list": branch_list,

            "bookcomment_form": bookcomment_form,
            "bookcomments": bookcoment,
    }))


## About 가지
@login_required(login_url='/accounts/login/')
def write_branch(request, book_info, parent_branch, cur_branch):
# fields = ('book', 'title', 'author', 'contents', 'parent_branch',)

    if request.method == "POST":
        branch_form = BranchCreationForm(request.POST)    
        print branch_form.errors
        if branch_form.is_valid():
            is_temporary = branch_form.cleaned_data['is_temporary']

            # 임시저장 상태에서 또 임시 저장 상태로 바뀐다면 수정해야함.
            # 임시저장 상태에서 그냥 저장 상태로 바뀐다면 고치고 저장해야 함.
            if cur_branch == '0':
                branch = branch_form.save()
            else:
                try:
                    branch = Branch.objects.get(id=cur_branch)
                    branch.title = branch_form.cleaned_data['title']
                    branch.contents = branch_form.cleaned_data['contents']
                except Branch.DoesNotExist:
                    pass
                
                if is_temporary: pass
                else: branch.is_temporary = False
                
                branch.save()
            # 임시저장 상태이고, 부모 노드가 없다면 책 상태의 루트노드를 저장하지 않는다.
            if is_temporary and parent_branch == '0':
                pass
            else:
                book = Book.objects.get(pk=book_info)
                book.root_branch = branch
                book.save()
            
            return HttpResponseRedirect('/')

    title = ''
    contents = ''
    if cur_branch != '0':
        try:
            branch = Branch.objects.get(id=cur_branch)
            title = branch.title
            contents = branch.contents
        except Branch.DoesNotExist:
            pass

        

    # if no branch in the book, send '0'
    branch_form = BranchCreationForm({'author': request.user,
                                      'book': book_info,
                                      'parent_branch': parent_branch,
                                      'title': title,
                                      'contents': contents})

    # Will Post parent_branch_id, Book_id
    return render_to_response('posts/write_branch.html', \
        RequestContext(request, {'form': branch_form,
                                 'book_info': book_info,
                                 'parent_branch': parent_branch,
                                 'cur_branch': cur_branch,} ))


@login_required(login_url='/accounts/login/')
def read_branch(request, branch_id):
    if request.method == "GET":
        try:       
            branch = Branch.objects.get(pk=branch_id)
        except Branch.DoesNotExist:
            raise Http404
        
        return render_to_response('posts/read_branch.html', \
            RequestContext(request, {'branch': branch,
                                     }))

    return HttpResponseRedirect('/')


@login_required(login_url='/accounts/login/')
def comment_branch(request, branch_id):
    pass


@login_required(login_url='/accounts/login/')
def like_branch(request, branch_id, like):
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        raise Http404

    # Like -> Dislike
    if like == '0':
        try:
            like = BranchLike.objects.get(liker=request.user, branch=branch)
        except BranchLike.DoesNotExist:
            raise Http404

        like.delete()
        branch.disliked(request.user)


    # Do Like
    else:
        like = BranchLike.objects.create(liker=request.user, branch=branch)
        like.save()
        branch.liked(request.user)

    return HttpResponseRedirect('/posts/get_bookinfo/' + str(branch.book.id))


@login_required(login_url='/accounts/login/')
def save_bookmark(request, branch_id):
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        raise Http404

    bookmark = Bookmark.objects.create(user=request.user, branch=branch)
    bookmark.save()

    return HttpResponseRedirect('/')