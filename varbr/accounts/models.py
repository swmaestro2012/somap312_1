from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #username = models.CharField(null=True, max_length=50)
    #email = models.CharField(null=True, max_length=50)

