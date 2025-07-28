from django.contrib import admin

from home.models import *

# Register your models here.
@admin.register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'position', 'is_active')  
    list_editable = ('position', 'is_active')  
    ordering = ('position',)  
    list_per_page = 20  
    search_fields = ('title', 'link')
    list_filter = ('is_active',)

    
admin.site.register(Category)
admin.site.register(NewsView)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_views', 'created_by', 'created_at', 'updated_by', 'updated_at') 

    def get_views(self, obj):
        return obj.views.count if hasattr(obj, 'views') else 0
    get_views.short_description = 'Views'
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('created_by', 'updated_by')
        return self.readonly_fields + readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

admin.site.register(News, NewsAdmin)
admin.site.register(SiteInfo)
admin.site.register(Default_pages)
admin.site.register(Subscriber)


admin.site.site_header = "The Chronify News Panel"
admin.site.site_title = "The Chronify Admin" 
admin.site.index_title = "Welcome to The Chronify"

admin.site.register(VideoPost)

