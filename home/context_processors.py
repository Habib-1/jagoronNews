
from home.templatetags.bangla_filters import convert_to_bangla_number
from .models import *
from datetime import datetime
from .models import News

def default(request):


    site_info = SiteInfo.objects.first()
    navbar_item = NavbarItem.objects.filter(is_active=True).order_by('position')
    default_pages = Default_pages.objects.all()

    current_date = datetime.now()
    bangla_date = f"{convert_to_bangla_number(current_date.day)}"

    return {

        'site_info': site_info,
        'navbar_item': navbar_item,
        'default_pages': default_pages,
        'bangla_date':bangla_date,
        'current_date': current_date,
    }



def top_headline_context(request):
    top_heading = News.objects.filter(category__name='Breaking News').order_by('-created_at')[:5]
    return {'top_heading': top_heading}