from accounts.models import UserProfile, FavoriteUser, UserComment
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(FavoriteUser)
admin.site.register(UserComment)