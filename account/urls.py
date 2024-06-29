from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('home/', views.home, name="home"),
    path('edit_items/', views.edit_items, name='edit_items'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]
