from django.shortcuts import render,get_object_or_404,redirect
from courses.models import Course,Video,Payment,UserCourse
from onlinecourses.settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse


import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
# Create your views here.
# Create your views here.
def courses(request):
 courses=Course.objects.all().order_by('-date')
 context={
    'courses':courses,
   
 }
 return render(request,'courses.html',context)

 ###########For single course############
def course_desc(request,slug):
   # course=Course.objects.get(slug  = slug)
   course = get_object_or_404(Course, slug=slug)
   serial_number  = request.GET.get('lecture')
   videos = course.video_set.all().order_by("serial_number")
   
   if serial_number is None:
        serial_number = 1 

   # video = Video.objects.get(serial_number = serial_number,course=course)
   video=get_object_or_404(Video,serial_number= serial_number,course=course)
   # is_verified_user_payment=False
   if (video.is_preview is False):
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user = user  , course = course)
               #  is_verified_user_payment=UserCourse.objects.get(user = user  , course = course).exists()
               # return is_verified_user_payment
            except:
                return redirect("checkout" , slug=course.slug)
   
   context={
    'course':course,
    'video':video,
    'videos':videos,
   #  'is_verified_user_payment':is_verified_user_payment
   }
   return render(request,'course.html',context)


##########For single course############
@login_required(login_url='login')
def checkout(request,slug):
   course = get_object_or_404(Course, slug=slug)
   # user=None
   # if not request.user.is_authenticated:
   #    return redirect('login')
   user=request.user
   order=None
   payment=None
   action=request.GET.get('action')
   is_user_course_exsists=UserCourse.objects.filter(user=user,course=course).exists()##############Tocheck if product is in Already in cart
   if action == 'create_payment':  #############creating razorpay order###############
      if not is_user_course_exsists:
         amount=int((course.price - ( course.price * course.discount * 0.01 )) * 100)
         currency='INR'
         receipt=f"webxpi-{int(time())}"                #############Any Random unique value genration ,In this we create fom time###########
         notes={
            'name':f'{user.first_name} {user.last_name}',
            'email':user.email,
         }

         order = client.order.create(  ##############creating order for razor-pay###############
                  {
                  'receipt' :receipt , 
                  'notes' : notes , 
                  'amount' : amount ,
                  'currency' : currency,
                  }
               )
         payment=Payment() ######creating paymenr object and assigning values in it###############
         payment.user=user
         payment.course=course
         payment.order_id=order.get('id')
         payment=payment.save()

   context={
      'course':course,
      'order':order,
      'payment':payment,
      'is_user_course_exsists':is_user_course_exsists,
   }
   return render(request,'checkout.html',context)



@login_required(login_url='login')
@csrf_exempt
def verify_payment(request):
   if request.method == "POST":
      data=request.POST
      try:
         client.utility.verify_payment_signature(data)
         razorpay_order_id = data['razorpay_order_id']
         razorpay_payment_id = data['razorpay_payment_id']
         payment = Payment.objects.get(order_id = razorpay_order_id)
         payment.payment_id  = razorpay_payment_id
         payment.status =  True 
         userCourse = UserCourse(user = payment.user , course = payment.course)
         userCourse.save()
         payment.user_course = userCourse
         payment.save()
         return redirect('payment_success')   
      except:
         return HttpResponse("Invalid Payment Details")

@login_required(login_url='login')
def payment_success(request):
   return render(request,'verify_payment.html')