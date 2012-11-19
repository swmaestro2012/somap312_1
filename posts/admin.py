from django.contrib import admin
from posts.models import Book, Branch, BookComment, BranchLike, Bookmark

admin.site.register(Book)
admin.site.register(Branch)
admin.site.register(BookComment)
admin.site.register(BranchLike)
admin.site.register(Bookmark)