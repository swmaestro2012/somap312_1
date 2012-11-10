# _*_ coding: utf-8 _*_
from django.db import models
from django.contrib.auth.models import User
import varbr.settings

import Image, uuid, os.path

def get_bookcoverimg_upload_path(instance, filename):
    size = 128, 128
    outfile = str(uuid.uuid1()) + ".thumbnail"
    
    try:
        im = Image.open(filename)
        im.thumbnail(size)
        im.save(outfile, "JPEG")
    except IOError:
        print "Cannot Create Thumbnail."

    filepath = 'coverimg/' + outfile

    return filepath


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
    #coverimg = models.ImageField(null=True, blank=True, upload_to='coverimg/')
    coverimg = models.ImageField(null=True, blank=True, upload_to=get_bookcoverimg_upload_path)
    synopsis = models.CharField(max_length=200, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    genre = models.IntegerField(default=1, choices=BOOK_GENRE_CHOICES)

    root_branch = models.ForeignKey('Branch', related_name="post_branch", null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ['-id']

    def get_coverimg(self):
        if self.coverimg == "":
            return varbr.settings.STATIC_URL + "default_cover.jpg"
        else:
            return varbr.settings.MEDIA_URL + self.coverimg.name


class Branch(models.Model):
    parent_branch = models.ForeignKey('self', null=True, blank=True)
    
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    #author_str = models.CharField(max_length=30)
    contents = models.TextField()

    time_created = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    is_temporary = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Branches"


    def check_to_like(self, user):
        branchlike_set = self.branchlike_set.filter(liker=user)
        return branchlike_set

    def liked(self, liker):
        branchlike_set = self.branchlike_set.select_related().all()
        self.like_count = branchlike_set.count()
        self.save()

    def disliked(self, disliker):
        self.branchlike_set.filter(liker=disliker).delete()
        branchlike_set = self.branchlike_set.select_related().all()
        self.like_count = branchlike_set.count()
        self.save()
        

class UserComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_user')
    #writer_str = models.CharField(max_length=30)
    writer = models.ForeignKey(User, related_name='user_writer')


class BookComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    #writer_str = models.CharField(max_length=30)
    book = models.ForeignKey(Book)
    class Meta:
        ordering = ['-id']


class BranchComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    #writer_str = models.CharField(max_length=30)
    branch = models.ForeignKey(Branch)


class BranchLike(models.Model):
    liker = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch)

    class Meta:
        verbose_name_plural = "Likes"
        unique_together = ("liker", "branch")

    def __unicode__(self):
        return unicode(self.liker)


class Bookmark(models.Model):
    branch = models.ForeignKey(Branch)
    user = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
