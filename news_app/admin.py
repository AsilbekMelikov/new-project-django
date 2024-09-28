from django.contrib import admin
from .models import News, Category, Contact

# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'publish_time', 'status']
    list_filter = ['status', 'publish_time', 'created_time', 'category']
    prepopulated_fields = {"slug": ('title',)}
    search_fields = ['category__name']
    ordering = ['publish_time', 'status']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Contact)


