from django.db import models
from django.contrib.auth.models import User
from .choices import CITY_CHOICES
from datetime import datetime
################User Profile######################
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    phone_number = models.CharField(blank=True, max_length=15)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile_pics',default='default.jpg', null=True)
    city = models.CharField(blank=True, max_length=20,default='Delhi',choices=CITY_CHOICES)
    updated_date = models.DateTimeField(default=datetime.now,blank=True,null=True)


    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
