from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length = 50 , null = False)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    description = models.TextField(max_length = 800 , null = True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False , default = 0) 
    active = models.BooleanField(default = False)
    thumbnail = models.ImageField(upload_to = "files/thumbnail") 
    date = models.DateTimeField(auto_now_add= True) 
    resource = models.FileField(upload_to = "files/resource")
    length = models.IntegerField(null=False)

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def get_url(self):
        return reverse('course_desc', args=[self.slug])

    def __str__(self):
        return self.name


class CourseProperty(models.Model): #########This is abstract table that is inherited by below tables because have same properties###
    
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    description  = models.CharField(max_length = 800 , null = False)

    class Meta : 
        abstract = True


class Tag(CourseProperty):
    pass
    
class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
    pass

class Video(models.Model):
    title  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length = 100 , null = False)
    is_preview = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class UserCourse(models.Model):
    user = models.ForeignKey(User , null = False , on_delete=models.CASCADE)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'

class Payment(models.Model):
    order_id = models.CharField(max_length = 400 , null = False)
    payment_id = models.CharField(max_length = 400)
    user_course = models.ForeignKey(UserCourse , null = True , blank = True ,  on_delete=models.CASCADE)
    user = models.ForeignKey(User ,  on_delete=models.CASCADE)
    course = models.ForeignKey(Course , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

