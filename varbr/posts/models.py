from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User)
    #creator_str = models.CharField(max_length=30)
    coverimg = models.ImageField(null=True, upload_to='/')
    synopsis = models.CharField(max_length=200, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    genre = models.IntegerField(default=0)

    #root_branch = models.ForeignKey(Branch, db_index=True)

    class Meta:
        verbose_name_plural = "Books"

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
