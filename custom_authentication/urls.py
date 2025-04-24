from django.urls import path , include 
from core import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include


from custom_authentication import views as custom_auth_views
urlpatterns = [

    path('logout', custom_auth_views.logout , name = "logout" ),
    path('profile', custom_auth_views.user_profile , name = "user_profile" ),
    path('add_profile', custom_auth_views.add_profile , name = "add_profile" ),
    path('update_profile', custom_auth_views.update_profile , name = "update_profile" ),
    path('change_password', custom_auth_views.change_password , name = "change_password" ),

    path('update_user', custom_auth_views.UpdateUser , name = "update_user" ),



    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='custom_authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="custom_authentication/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='custom_authentication/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset", custom_auth_views.password_reset_request, name="password_reset")



]

