from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),


]