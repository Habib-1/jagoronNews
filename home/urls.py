from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/details/<int:pk>/',views.news_details,name='news_details'),
    path('news/all/', views.news_by_category, name='news_by_cat'),
    path('category/news/<int:cat_id>/', views.news_by_category,name='news_by_cat'),
    path('today/news/', views.today_news, name='today_news'),
    path('breaking/news/', views.breaking_news, name='breaking_news'),
    path('policy/<str:link>/',views.policy_detail,name='policy_detail'),
    path('subscribe/', views.subscribe_form, name='subscribe'),
    path('subscribe/form/',views.subscribe_form,name='subscribe_form'),
]