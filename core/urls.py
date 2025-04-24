"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500

from django.contrib.sitemaps.views import sitemap


urlpatterns = [

    path('', core_views.home , name = "home" ),
    path('about', core_views.about , name = "about" ),
    path('marque', core_views.marque , name = "marque" ),
    path('blog', core_views.mini_blog , name = "mini_blog" ),
    path('blog/<slug:slug>', core_views.mini_blog_detail , name = "mini_blog_detail" ),



    path('faq', core_views.faq , name = "faq" ),
    path('404', core_views.r_404_view,name="404"),
    path('contact', core_views.contact , name = "contact" ),

    path('open_quiz_list', core_views.open_quiz_list , name = "open_quiz_list" ),
    path('score_board', core_views.score_board , name = "score_board" ),
    path('free_score_board', core_views.free_score_board , name = "free_score_board" ),



    path('policy', core_views.policy , name = "policy" ),

    path('terms', core_views.terms , name = "terms" ),




    path('login', core_views.login , name = "login" ),

    path('register', core_views.user_registeration , name = "register" ),

    path('authenicate/', include("custom_authentication.urls")),

    # path('payment_status_api/', core_views.payment_status_api , name = "payment_status_api" ),
    path('payment_status_api', core_views.payment_status_api , name = "payment_status_api" ),


    path('take_exam', core_views.take_exam , name = "take_exam" ),

    path('direct_take_exam/<int:order_id>', core_views.direct_take_exam , name = "direct_take_exam" ),


    # path('user_quiz_start', core_views.user_quiz_start , name = "user_quiz_start" ),
    path('user/', include("userdashboard.urls")),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

