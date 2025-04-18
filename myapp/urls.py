from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    # path('home/',home,name='home'),
    path('course/',course,name='course'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
   path("blog/", blog_list,name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path("log_in/", log_in, name='log_in'),
    path("register/", register, name='register'),
    path('log_out/', log_out, name='log_out'),
    path('payment/<int:id>',payment,name='payment'),
    path("initiate", initkhalti, name="initiate"),
    path("payment-success",payment_success, name="payment_success"), 
    path("payment-failure",payment_failure, name="payment_failure"),

]
