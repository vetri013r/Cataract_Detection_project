
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.upload_image,name='home' ),
    path('about/',views.about),
    path('home/report/',views.Report,name='upload_success'),
]