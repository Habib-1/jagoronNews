from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_page, name='news_page'),
    path('news/detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('default-pages/<str:link>/', views.default_page_detail, name='default_page_detail'),
    path('jagoron-1lakh/', views.generate_photo, name='generate_photo'),

    path('search/', views.search_news, name='search_news'),
    

    path('s/<str:short_code>/', views.redirect_short_url, name='redirect_short_url'),
    path('api/create-short-url/', views.create_short_url, name='create_short_url'),
]