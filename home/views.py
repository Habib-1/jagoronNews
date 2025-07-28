from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import date
from home.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.contrib import messages
import requests
import io
import base64
from home.templatetags.bangla_filters import convert_to_bangla_number
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter
import random
from datetime import date
from datetime import datetime
from django.db.models import Count
import json
from django.shortcuts import render, get_object_or_404
from .models import News, Category,NavbarItem
from django.db.models import Count
# Create your views here.

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    category=Category.objects.all()
    navbar = NavbarItem.objects.filter(is_active=True).annotate(news_count=Count('news'))
    top_heading=News.objects.filter(category__name='Breaking News').order_by('-created_at')[:5]
    selected_section_id = request.GET.get('section')
    news_items = None

    if selected_section_id:
        try:
            selected_section = NavbarItem.objects.get(id=selected_section_id)
            news_items = News.objects.filter(section=selected_section)
        except NavbarItem.DoesNotExist:
            selected_section = None
            news_items = News.objects.none()
    else:
        selected_section = None
        news_items = News.objects.all()

    last_news = News.objects.order_by('-id').first()
    live_news = News.objects.filter(category__name="Live").last()
    international = News.objects.all().filter(category__name="International")[0:4]
    national = News.objects.all().filter(category__name="National")[0:5]
    updated_news = News.objects.all().order_by('-id')[1:10]
    live_category = Category.objects.get(name="Live")
    elected_category = Category.objects.get(name="Elected News")
    # last_elected_news = News.objects.filter(category=elected_category).order_by('-id').first()
    elected_news = News.objects.filter(category=elected_category).order_by('-id')[0:8]
    sections = NavbarItem.objects.filter(is_active=False).exclude(title="Top Readed").order_by('position')
    most_read_news_ids = list(
        NewsView.objects.order_by('-count')[:8]
        .values_list('news_id', flat=True)
    )

    most_read_news = [News.objects.get(id=news_id) for news_id in most_read_news_ids]
    current_date = datetime.now()
    video_post = VideoPost.objects.all().order_by("-id")
    today = now().date()
    todays_most_viewed_news = (
        NewsView.objects.filter(news__created_at__date=today)
        .order_by('-count')[:4]
    )

    current_url = request.build_absolute_uri()
  # added by me
    city = 'Dhaka'
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    


    context = {
        'navbar': navbar,
        'news_items': news_items,
        'selected_section': selected_section,
        'international': international,
        'updated_news': updated_news,
        'live_category': live_category,
        'elected_news': elected_news,
        # 'last_elected_news': last_elected_news,
        'sections': sections,
        'most_read_news': most_read_news,
        'last_news': last_news,
        'current_date': current_date,
        'video_post':video_post,
        'todays_most_viewed_news': [news_view.news for news_view in todays_most_viewed_news],
        'current_url': current_url,
        'national':national,
        'category' : category,
        'location': data['name'],
        'temperature': data['main']['temp'],
        'min_temp': data['main']['temp_min'],
        'max_temp': data['main']['temp_max'],
        'humidity': data['main']['humidity'],
        'condition': data['weather'][0]['main'],   # e.g., "Clear", "Clouds"
        'icon': data['weather'][0]['icon']  # e.g., "01d"
        
    }

    if last_news == live_news:
        context['live_news'] = live_news

    return render(request, 'home/home.html', context)



def news_details(request, pk):
    news = get_object_or_404(News, pk=pk)
    current_category_ids = news.category.values_list('pk', flat=True)
    related_news_list = News.objects.filter(category__in=list(current_category_ids)).exclude(pk=news.pk).distinct()[:5] 
    navbar = NavbarItem.objects.filter(is_active=True).annotate(news_count=Count('news'))
    elected_category = Category.objects.get(name="Elected News")
    elected_news = News.objects.filter(category=elected_category).order_by('-id')[1:5]
    updated_news = News.objects.all().order_by('-id')[5:9]
    # you_may_like = News.objects.filter(category__in=list(current_category_ids)).exclude(pk=news.pk).distinct()[6:10] 
    category=Category.objects.all()
    most_read_news_ids = list(
        NewsView.objects.order_by('-count')[:4]
        .values_list('news_id', flat=True)
    )

    most_read_news = [News.objects.get(id=news_id) for news_id in most_read_news_ids]
    context = {
        'news': news,
        'related_news_list': related_news_list,
        'navbar':navbar,
        'elected_news':elected_news,
        'updated_news':updated_news,
        # 'you_may_like':you_may_like,
        'category' : category,
        'most_read_news': most_read_news
    }
    return render(request, 'pages/news_details.html', context)

def news_by_category(request, cat_id=None):
    all_category = NavbarItem.objects.filter(is_active=True)

    if cat_id:
        category = get_object_or_404(NavbarItem, id=cat_id)
        news_list = News.objects.filter(section=category).order_by('-created_at')
    else:
        category = None
        news_list = News.objects.all().order_by('-created_at')

    paginator = Paginator(news_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'all_category': all_category,
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'pages/news_by_category.html', context)

def today_news(request):
    today = date.today()
    news_list = News.objects.filter(created_at__date=today).order_by('created_at')
    paginator = Paginator(news_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    message="📭 No news published today.Please check back later for the latest updates."
    context = {
        'page_obj': page_obj,
        'message' : message,
        
    }
    return render(request,'pages/today_news.html',context)

def breaking_news(request):
    news_list = News.objects.filter(category__name='Breaking News')
    paginator = Paginator(news_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    message="🚨 No breaking news at the moment.Stay tuned — we’ll update as soon as news breaks."
    context = {
        'page_obj': page_obj,
        'message' : message,
        
    }
    return render(request,'pages/today_news.html',context)

def policy_detail(request,link):
    policy=get_object_or_404(Default_pages,link=link)
    return render(request, 'pages/footer_template.html',context={ 'data':policy, })

def subscribe_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, "You have already subscribed.")
        else:
            Subscriber.objects.create(name=name, email=email)
            messages.success(request, "Subscription successful!")

        return redirect("home")

    return render(request, "pages/subscribe.html")

def subscribe_view(request):
    return render(request, 'pages/subscribe.html')