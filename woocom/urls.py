from django.urls import path

from woocom import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:d_id>/', views.detail, name='detail'),
]
