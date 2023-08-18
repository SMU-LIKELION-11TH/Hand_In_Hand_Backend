from django.urls import path

from user import views

urlpatterns = [
    path('', views.user_signup, name="user_create"),
    path('emailvalidation/', views.email_validation, name="email_validation"),
    path('verify/<int:pk>/<str:token>/', views.verify_email, name='verify_email'),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('find_email/',views.find_email,name="find_email"),
    path('password_reset/',views.password_reset,name="password_reset"),
    path('check_email/',views.check_email,name="check_email"),
    path('check_nickname/', views.check_nickname, name="check_nickname"),
    path('info/', views.user_info, name="user_info"),
    path('attend_check/', views.attend_check, name="attend_check"),
    path('attend/',views.attend, name="show_attend"),
    path('update_info/', views.update_info, name="update_info"),
    path('delete/user/', views.delete_user, name="delete_user"),
    path('emailvalidationP/', views.find_password, name="find_password"),
    path('check_code/', views.check_code_email,name="check_code_email"),
    path('verify_page', views.verify_page, name="verify_page"),
    path('verify_page_error',views.verify_page_error, name="verify_page_error")
]