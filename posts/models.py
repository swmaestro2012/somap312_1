# _*_ coding: utf-8 _*_
from django.db import models
from django.contrib.auth.models import User
from varbr import settings

import Image, uuid, os.path


def get_bookcoverimg_upload_path(instance, filename):
    # TODO: Original File must be deleted. Must be used thumbnail file.
    size = 128, 128
    fname = str(uuid.uuid1()) + '.jpg'
    outfile = settings.PROJECT_PATH + '/media/coverimg/thumbnail/' + fname
    try:
        im = Image.open(instance.coverimg)
        im.thumbnail(size)
        im.save(outfile , "JPEG")
    except: # Should Correct 32-64 bit compatible
        pass 

    return 'coverimg/' + fname

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
    creator_str = models.CharField(max_length=20)
    coverimg = models.ImageField(null=True, blank=True, upload_to=get_bookcoverimg_upload_path)
    synopsis = models.CharField(max_length=200, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    genre = models.IntegerField(default=1, choices=BOOK_GENRE_CHOICES)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    
    
    root_branch = models.ForeignKey('Branch', related_name="post_branch", null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "Books"

    def get_coverimg(self):
        if self.coverimg == "":
            return settings.STATIC_URL + "default_cover.jpg"
        else:
            # 9 is length of "coverimg/"
            return settings.MEDIA_URL + "coverimg/thumbnail/" + self.coverimg.name[9:]


class Branch(models.Model):
    parent_branch = models.ForeignKey('self', null=True, blank=True)
    
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    author_str = models.CharField(max_length=20)
    contents = models.TextField()

    time_created = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    is_temporary = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Branches"


    def check_to_like(self, user):
        try:
            branchlike_set = self.branchlike_set.get(liker=user)
            return branchlike_set
        except:
            return ""

    def set_liked(self, liker):
        branchlike_set = self.branchlike_set.select_related().all()
        self.like_count = branchlike_set.count()
        self.save()

    def set_disliked(self, disliker):
        self.branchlike_set.filter(liker=disliker).delete()
        branchlike_set = self.branchlike_set.select_related().all()
        self.like_count = branchlike_set.count()
        self.save()
        

class BookComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    writer_str = models.CharField(max_length=20)
    book = models.ForeignKey(Book)
    class Meta:
        ordering = ['-id']


class BranchComment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User)
    writer_str = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch)

    class Meta:
        ordering = ['-id']

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


class Attachment(models.Model):
    filename = models.CharField(max_length=255)
    filetype = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/")
    branch = models.ForeignKey(Branch)
