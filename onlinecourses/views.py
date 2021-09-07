from django.shortcuts import render,redirect
from courses.models import Course,UserCourse
# Create your views here.
# Create your views here.
def home(request):
 courses=Course.objects.all().order_by('-date')[:3]
 context={
    'courses':courses,
 }
 return render(request,'home.html',context)

