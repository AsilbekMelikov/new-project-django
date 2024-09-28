from django.urls import path
from .views import news_list_view, news_detail_view, HomePageView, ContactPageView, \
    LocalNewsView, WorldNewsView, TechnologyNewsView, SportNewsView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path('news/', news_list_view, name='news_list'),
    path('news/<slug:news_slug>', news_detail_view, name='news_details'),
    path('contact-us/', ContactPageView.as_view(), name="contact_page"),
    path("news/local/", LocalNewsView.as_view(), name='Mahalliy'),
    path("news/world/", WorldNewsView.as_view(), name='Xorij'),
    path("news/technology/", TechnologyNewsView.as_view(), name="Texnologiya"),
    path("news/sport/", SportNewsView.as_view(), name="Sport")
]