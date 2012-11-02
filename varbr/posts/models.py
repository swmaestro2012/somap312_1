# -*- coding: utf-8 -*-
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
    BOOK_GENRE_CHOICES = (
        (1, '게임'),
        (5, '공포'),
        (10, '로맨스'),
        (15, '무협'),
        (20, '소설'),
        (25, '수필'),
        (30, '시'),
        (35, '시나리오/희곡'),
        (40, '아동'),
        (45, '역사'),
        (50, '전쟁'),
        (55, '추리'),
        (60, '판타지'),
        (65, '패러디'),
        (70, '팬픽'),
        (75, '평론'),
        (80, '퓨전'),
        (85, 'BL'),
        (90, 'Lt Novel'),
        (95, 'SF'),
    )
    
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User)
    #creator_str = models.CharField(max_length=30)
    coverimg = models.ImageField(null=True, upload_to='coverimg/')
    synopsis = models.CharField(max_length=200, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    genre = models.IntegerField(default=1, choices=BOOK_GENRE_CHOICES)

    # root_branch = models.ForeignKey(Branch, null=True)
    root_branch = models.IntegerField(default=0, null=True)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ['-id']

    def get_coverimg(self):
        if self.coverimg == "":
            return varbr.settings.STATIC_URL + "default_cover.jpeg"
        else:
            return varbr.settings.MEDIA_URL + self.coverimg.name

class Branch(models.Model):
    #parent_branch = models.ForeignKey('self', null=True, blank=True)
    parent_branch = models.IntegerField(default=0, null=True)
    
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    #author_str = models.CharField(max_length=30)
    contents = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Branches"


class UserComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='usercomment_user')
    #writer_str = models.CharField(max_length=30)
    writer = models.ForeignKey(User, related_name='usercomment_writer')


class BookComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    #writer_str = models.CharField(max_length=30)
    book = models.ForeignKey(Book)


class BranchComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    #writer_str = models.CharField(max_length=30)
    branch = models.ForeignKey(Branch)


class Like(models.Model):
    liker = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch)

    class Meta:
        verbose_name_plural = "Likes"
