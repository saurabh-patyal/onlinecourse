from django.urls import path
from . import views

urlpatterns = [
     path('', views.courses , name='courses'),
     path('course/<slug:slug>/', views.course_desc, name='course_desc'),
     path('checkout/<slug:slug>/', views.checkout, name='checkout'),
     path('mycourses', views.mycourses, name='mycourses'),
     path('verify_payment', views.verify_payment, name='verify_payment'),
     path('payment_success', views.payment_success, name='payment_success'),
     
     
]