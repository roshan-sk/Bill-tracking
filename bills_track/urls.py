from django.urls import path
from . import views

urlpatterns = [
    path('bills/', views.bill_list_view, name='bill_list'),
    path('bills/create/', views.bill_create_view, name='bill_create'),
    path('bills/<int:pk>/update/', views.bill_update_view, name='bill_update'),
    path('bills/<int:pk>/delete/', views.bill_delete_view, name='bill_delete'),
    # path('download-pdf/', views.download_pdf, name='download_pdf'),
]
