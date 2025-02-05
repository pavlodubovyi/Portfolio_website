from django.urls import path, include
from pages import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('hire/', views.hire, name='hire'),
    path('needful_things/', include('needful_things.urls')),
]
