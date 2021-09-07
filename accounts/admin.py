from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))

    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)