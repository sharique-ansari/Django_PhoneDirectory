from django.urls import path

from . import views
app_name = "contacts"

urlpatterns = [
    path('', views.user_upload, name='upload'),
    path('user/<int:user_id>/', views.details, name='detail'),
    path('retrieve/', views.retrieve, name = 'retrieve')
]