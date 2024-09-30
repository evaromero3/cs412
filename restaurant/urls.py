
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # Define your URL patterns here, for example:
    path('', views.main, name='main'),  # Main page
    path('order/', views.order, name='order'),  # orders page
    path('confirmation/', views.confirmation, name='confirmation'),  # confirmation page
    
]