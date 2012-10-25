from django.db import models
from django.contrib.auth.models import User

import varbr.settings
'''
import uuid

def get_book_coverimg_upload_path(instance, filename):
    ext = "jpg"
    print 'abcd'
    if "." in filename:
        ext = filename.split(".")[-1]
    newfilename = str(uuid.uuid1()) + "." + ext
    newfilepath = 'coverimg/' + newfilename

    return newfilepath
'''
class Book(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User)
    #creator_str = models.CharField(max_length=30)
    coverimg = models.ImageField(null=True, upload_to='coverimg/')
    synopsis = models.CharField(max_length=200, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    genre = models.IntegerField(default=0)

    #root_branch = models.ForeignKey(Branch, db_index=True)

    class Meta:
        verbose_name_plural = "Books"

    def get_coverimg(self):
        if self.coverimg == "":
            return varbr.settings.STATIC_URL + "default_cover.jpeg"
        else:
            return varbr.settings.MEDIA_URL + self.coverimg.name

class Branch(models.Model):
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    #author_str = models.CharField(max_length=30)
    contents = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    parent_branch = models.ForeignKey('self')

    class Meta:
        verbose_name_plural = "Branches"

class Comment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    #writer_str = models.CharField(max_length=30)
    branch = models.ForeignKey(Branch)

    class Meta:
        verbose_name_plural = "Comments"

class Like(models.Model):
    liker = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch)

    class Meta:
        verbose_name_plural = "Likes"
