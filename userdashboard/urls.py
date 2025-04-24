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
from userdashboard import views as user_dash_views
from django.core.paginator import Paginator



urlpatterns = [
    path('', user_dash_views.user_dashboard , name = "user_dashboard" ),
    # path('test_dashboard', user_dash_views.test_dashboard , name = "test_dashboard" ),

    path('play_quiz', user_dash_views.open_quiz , name = "open_quiz" ),
    path('start_quiz', user_dash_views.start_quiz , name = "start_quiz" ),
    path('attempt_quiz/<int:id>', user_dash_views.attempt_quiz , name = "attempt_quiz" ),

    path('result_board', user_dash_views.result_board , name = "result_board" ),
    path('played_history', user_dash_views.played_list , name = "played_list" ),
    path('free_played_history', user_dash_views.free_played_list , name = "free_played_list" ),


    path('start_quiz_history', user_dash_views.player_start_quiz_list , name = "start_quiz_history" ),

    path('check_payment_varified', user_dash_views.check_payment_varified , name = "check_payment_varified" ),




    path('submit_quiz/<int:id>', user_dash_views.submit_quiz , name = "submit_quiz" ),
    path('skip_quiz', user_dash_views.skip_quiz , name = "skip_quiz" ),
 
    path('submit_quiz_result', user_dash_views.submit_quiz_result , name = "submit_quiz_result" ),

    path('paid_payment/<int:id>', user_dash_views.paid_payment , name = "paid_payment" ),
    # path('payment_successfull/<int:id>', user_dash_views.payment_successfull , name = "payment_successfull" ),





    path('test_payment', user_dash_views.test_payment , name = "test_payment" ),






    # path('payment_status_api/<str:PaymentType>/<str:TotalPrice>/<str:OrderId>/<str:ResultCode>/<str:TxnId>/<str:Checksum>', user_dash_views.payment_status_api , name = "payment_status_api" ),

    # path('payment_callback_api/<str:amp;TotalPrice>/<str:TotalPrice>/<str:OrderId>/<str:ResultCode>/<str:TxnId>/<str:Checksum>', user_dash_views.payment_status_api , name = "payment_status_api" ),




    

]
