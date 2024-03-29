# _*_ coding: utf-8 _*_
from accounts.models import UserProfile
from models import Book, Branch, BookComment, BranchLike, Bookmark, BranchComment
from forms import BookCreationForm, BranchCreationForm, BookCommentForm, BranchCommentForm

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

############# BOOKS
INDEX_PAGE_BOOKS = 5
BOOK_PAGINATION = 4

BEST_BOOK_TYPE = 1
NEW_BOOK_TYPE = 2
MY_BOOK_TYPE = 3

############# BRANCHES
BRANCH_PAGINATION = 4

MY_BRANCHED_TYPE = 1
MY_BRANCHING_TYPE = 2
MY_BOOKMARK_TYPE = 3
#############

@login_required
def main_page(request):
    best_books = Book.objects.order_by("-like_count")[:INDEX_PAGE_BOOKS]

    return render_to_response('index.html', RequestContext(request, {
            "best_books": best_books,
        }))

# 명예의전당
@login_required
def recommend_list(request):
    book_list = Book.objects.exclude(root_branch=None).order_by("-like_count")
    paginator = Paginator(book_list, BOOK_PAGINATION)

    page = request.GET.get("page")

    if page == None:
        page = 1
    else:
        page = int(page)

    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    if page == 1: 
        return render_to_response('posts/book_list.html', RequestContext(request, {
                'book_list': book_list,
                'page': page+1,
                'type': BEST_BOOK_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))
    else:
        return render_to_response('posts/books.html', RequestContext(request, {
            'book_list': book_list,
            'page': page+1,
            'type': BEST_BOOK_TYPE,
            'is_lastpage': page==paginator.num_pages,
        }))


# 최신작
@login_required
def show_newlist(request):
    book_list = Book.objects.exclude(root_branch=None).order_by("-id")
    paginator = Paginator(book_list, BOOK_PAGINATION)

    page = request.GET.get("page")

    if page == None:
        page = 1
    else:
        page = int(page)

    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        page=-1

    if page == 1: 
        return render_to_response('posts/book_list.html', RequestContext(request, {
                'book_list': book_list,
                'page': page+1,
                'type': NEW_BOOK_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))
    else:
        return render_to_response('posts/books.html', RequestContext(request, {
            'book_list': book_list,
            'page': page+1,
            'type': NEW_BOOK_TYPE,
            'is_lastpage': page==paginator.num_pages,
        }))

# 검색
@login_required
def search_book(request):
    query = request.GET.get("query")
    genre = request.GET.get("genre")

    print "query=%s, genre=%s" % (query, genre)

    if query is None and genre is None:
        return render_to_response('posts/search_book.html', RequestContext(request))

    if query and genre:
        book_list = Book.objects.filter(title__contains=query, genre=genre).order_by("-id")
    elif query:
        book_list = Book.objects.filter(title__contains=query).order_by("-id")
    elif genre:
        book_list = Book.objects.filter(genre=genre).order_by("-id")

    return render_to_response('posts/search_book.html', RequestContext(request, {
            "book_list": book_list,
        }))

# 책갈피 MY_BOOKMARK_TYPE
@login_required
def show_bookmarks(request):
    bookmark_list = Bookmark.objects.filter(user=request.user).order_by("-id")
    paginator = Paginator(bookmark_list, BRANCH_PAGINATION)

    page = request.GET.get("page")

    if page == None:
        page = 1
    else:
        page = int(page)

    try:
        bookmark_list = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        page=-1

    if page == 1: 
        return render_to_response('posts/branch_list.html', RequestContext(request, {
                'bookmark_list': bookmark_list,
                'page': page+1,
                'type': MY_BOOKMARK_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))
    else:
        return render_to_response('posts/branches.html', RequestContext(request, {
            'bookmark_list': bookmark_list,
            'page': page+1,
            'type': MY_BOOKMARK_TYPE,
            'is_lastpage': page==paginator.num_pages,
        }))


# 심은 책
@login_required
def get_author_books(request, author_id):
    book_list = Book.objects.filter(creator=author_id).order_by("-id")

    paginator = Paginator(book_list, BOOK_PAGINATION)

    page = request.GET.get("page")

    if page == None:
        page = 1
    else:
        page = int(page)

    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        page=-1

    if page == 1: 
        return render_to_response('posts/book_list.html', RequestContext(request, {
                'book_list': book_list,
                'page': page+1,
                'type': MY_BOOK_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))
    else:
        return render_to_response('posts/books.html', RequestContext(request, {
            'book_list': book_list,
            'page': page+1,
            'type': MY_BOOK_TYPE,
            'is_lastpage': page==paginator.num_pages,
        }))


# 작성한 가지
@login_required
def get_author_branches(request, author_id):
    branch_list = Branch.objects.filter(author=author_id, is_temporary=False)

    paginator = Paginator(branch_list, BRANCH_PAGINATION)

    page = request.GET.get("page")

    if page == None:
        page = 1
    else:
        page = int(page)

    try:
        branch_list = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    if page == 1:
        return render_to_response('posts/branch_list.html', RequestContext(request, {
                'branch_list': branch_list,
                'page': page+1,
                'type': MY_BRANCHED_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))
    else:
        return render_to_response('posts/branches.html', RequestContext(request, {
                'branch_list': branch_list,
                'page': page+1,
                'type': MY_BRANCHED_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))


# 댓글 한 잎
####

# 책심기
@login_required
def create_book(request):
    if request.method == "POST":
        book_form = BookCreationForm(request.POST, request.FILES)
        print book_form.errors
        if book_form.is_valid():
            book = book_form.save(commit=False)

            # Check
            if book.creator != request.user:
                raise Http404            

            book.save()
            return HttpResponseRedirect('/posts/get_bookinfo/' + str(book.id))

    book_form = BookCreationForm({ 'creator': request.user })
    
    return render_to_response('posts/create_book.html', \
        RequestContext(request, { 'form': book_form } ))


# 작성중인 가지
@login_required
def working_branch(request):
    branch_list = Branch.objects.filter(author=request.user, is_temporary=True).order_by("-id")

    paginator = Paginator(branch_list, BRANCH_PAGINATION)

    page = request.GET.get("page")

    if page == None:
        page = 1
    else:
        page = int(page)

    try:
        branch_list = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    if page == 1:
        return render_to_response('posts/branch_list.html', RequestContext(request, {
                'branch_list': branch_list,
                'page': page+1,
                'type': MY_BRANCHING_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))
    else:
        return render_to_response('posts/branches.html', RequestContext(request, {
                'branch_list': branch_list,
                'page': page+1,
                'type': MY_BRANCHING_TYPE,
                'is_lastpage': page==paginator.num_pages,
            }))


# 계정 설정

####################


## 책 정보
@login_required
def get_bookinfo(request, book_id):
# fields = ('book', 'writer', 'text',)
# TODO: ajax and 함수 분리.
    try:
        book_info = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Http404


    if request.method == "POST":
        bookcomment_form = BookCommentForm(request.POST)
        print bookcomment_form.errors
        if bookcomment_form.is_valid():
            bookcomment = bookcomment_form.save(commit=False)

            if request.user != bookcomment.writer:
                raise Http404

            bookcomment.save()

            return HttpResponse('');
            #return HttpResponseRedirect('/posts/get_bookinfo/' + book_id)

    branch_list = Branch.objects.filter(book=book_id, is_temporary=False)

    tree_data =[]
    for branch in branch_list:
        #if branch.check_to_like(request.user):
        #    branch.is_liked = True
        try:
            tree_data.append({
                "bid": branch.id,
                "pid": branch.parent_branch.id,
                "uid": branch.author.id,
                "point": branch.like_count,
                "uimage": branch.author.get_profile().get_profileimg()
            })
        except AttributeError: # If There have no parent branch
            tree_data.append({
                "bid": branch.id,
                "pid": 0,
                "uid": branch.author.id,
                "point": branch.like_count,
                "uimage": branch.author.get_profile().get_profileimg()
            })
    tree_data = json.dumps(tree_data)
    bookcomments = BookComment.objects.filter(book=book_id)
    
    bookcomment_form = BookCommentForm({'book': book_info,
                                        'writer' : request.user })

    return render_to_response("posts/get_bookinfo.html", RequestContext(request, {
            "user": request.user.id,
            "book_info": book_info,
            "branch_list": branch_list,
            "tree_data": tree_data,

            "bookcomment_form": bookcomment_form,
            "comments": bookcomments,
    }))

# 브랜치 정보
@login_required
def get_branchinfo(request, branch_id):
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        raise Http404

    # TODO: 파일 분리 하기
    if request.method == "POST":
        branchcomment_form = BranchCommentForm(request.POST)
        print branchcomment_form.errors
        if branchcomment_form.is_valid():
            bf = branchcomment_form.save(commit=False)


            if bf.writer != request.user:
                raise Http404

            bf.save()
            branch.comment_count = BranchComment.objects.filter(branch=bf.branch).count()
            branch.save()
            return HttpResponse(branch.comment_count);

    branch_comments = BranchComment.objects.filter(branch=branch_id)

    branchcomment_form = BranchCommentForm({'branch': branch,
                                        'writer' : request.user })
    
    if branch.check_to_like(request.user):
        branch.is_liked = True

    return render_to_response("posts/get_branchinfo.html", RequestContext(request, {
            "branch": branch,
            "comments": branch_comments,

            "branchcomment_form": branchcomment_form,
        }))


@login_required
def show_mybookcomment(request):
    book = Book.objects.filter(creator=request.user.id)
    bookcomments = BookComment.objects.filter(book__in=book)
    print bookcomments

    return render_to_response('posts/show_comments.html', RequestContext(request, {
            "comments": bookcomments,
    }))


@login_required
def show_mybranchcomment(request):
    branch = Branch.objects.filter(author=request.user.id)
    branchcomments = BranchComment.objects.filter(branch__in=branch)
    print branchcomments

    return render_to_response('posts/show_comments.html', RequestContext(request, {
            "comments": branchcomments,
    }))


# 책 코멘트
@login_required
def show_bookcomment(request, book_id):
    bookcomments = BookComment.objects.filter(book=book_id)

    return render_to_response('posts/show_comments.html', RequestContext(request, {
            "comments": bookcomments,
    }))


# 브랜치 코멘트
@login_required
def show_branchcomment(request, branch_id):
    branchcomments = BranchComment.objects.filter(branch=branch_id)

    return render_to_response('posts/show_comments.html', RequestContext(request, {
            "comments": branchcomments,
    }))


## About 가지
@login_required
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
                branch = branch_form.save(commit=False)
                if request.user != branch.author:
                    raise Http404
                branch.save()
            else:
                try:
                    branch = Branch.objects.get(id=cur_branch)
                    branch.title = branch_form.cleaned_data['title']
                    branch.contents = branch_form.cleaned_data['contents']
                except Branch.DoesNotExist:
                    pass
                
                if is_temporary: pass
                else: branch.is_temporary = False
                
                if request.user != branch.author:
                    raise Http404

                branch.save()
            # 임시저장 상태이고, 부모 노드가 없다면 책 상태의 루트노드를 저장하지 않는다.
            if is_temporary and parent_branch == '0':
                pass
            else:
                book = Book.objects.get(pk=book_info)
                book.root_branch = branch
                book.save()
            
            return HttpResponseRedirect('/posts/get_bookinfo/' + book_info)

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


@login_required
def read_branch(request, branch_id):
    if request.method == "GET":
        try:       
            branch = Branch.objects.get(pk=branch_id)
            next_branches = Branch.objects.filter(parent_branch=branch_id)
        except Branch.DoesNotExist:
            raise Http404
        
        return render_to_response('posts/read_branch.html', \
            RequestContext(request, {'branch': branch,
                                    'next_branches' : next_branches,
                                     }))

    return HttpResponseRedirect('/')


@login_required
def comment_branch(request, branch_id):
    pass


@login_required
def like_branch(request, branch_id, like):
    try:
        branch = Branch.objects.get(id=branch_id)
        book = Book.objects.get(id=branch.book.id)
        userprofile = UserProfile.objects.get(user=branch.author.id)
    except Branch.DoesNotExist:
        raise Http404
    except Book.DoesNotExist:
        raise Http404
    except UserProfile.DoesNotExist:
        raise Http404

    # Like -> Dislike
    if like == '0':
        try:
            like = BranchLike.objects.get(liker=request.user, branch=branch)
        except BranchLike.DoesNotExist:
            pass #raise Http404

        like.delete()
        branch.set_disliked(request.user)

        # Mustn't User +1, Have to number 
        # synchronazation? get_num()
        book.like_count = book.like_count - 1
        userprofile.points = userprofile.points - 1
        book.save()
        userprofile.save()

    # Do Like
    else:
        try:
            like = BranchLike.objects.create(liker=request.user, branch=branch)
        except: #TODO: Integrity Error, Because liker and branch are unique
            pass
        branch.set_liked(request.user)
        
        book.like_count = book.like_count + 1
        userprofile.points = userprofile.points + 1
        book.save()
        userprofile.save()

    #return HttpResponseRedirect('/posts/get_bookinfo/' + str(branch.book.id))
    return HttpResponse(branch.like_count)



@login_required
def save_bookmark(request, branch_id):
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        raise Http404

    bookmark = Bookmark.objects.create(user=request.user, branch=branch)
    bookmark.save()

    return HttpResponseRedirect('/posts/read_branch/' + branch_id)