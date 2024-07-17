from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="register"),
    path('log/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('home/', views.home, name="home"),
    path('add_item/', views.add_item, name='add_item'),  # Correct URL pattern
    path('edit_items/', views.edit_items, name='edit_items'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),

    path('register/', views.register_user, name="register"),
    path('verify/<str:masked_email>/', views.verify_otp, name='verify'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('webpage/', views.webpage, name="webpage"),
    # path('password_reset/', views.password_reset, name="password_reset"),

    path('forgot_password/', views.forgot_password,name='forgot_password'),
    path('reset_password/<str:encrypted_email>/', views.reset_password, name='reset_password'),
    path('reset_password_submit/', views.reset_password_submit, name='reset_password_submit'),
]
