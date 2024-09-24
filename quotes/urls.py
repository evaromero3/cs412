
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # Define your URL patterns here, for example:
    path('', views.index, name='index'),  # Main page
    path('quote/', views.quote, name='quote'),  # Random quote page
    path('show_all/', views.show_all, name='show_all'),  # Show all quotes page
    path('about/', views.about, name='about'),  # About page
]