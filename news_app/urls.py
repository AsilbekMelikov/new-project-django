from django.urls import path
from .views import news_list_view, news_detail_view, HomePageView, ContactPageView, \
    LocalNewsView, WorldNewsView, TechnologyNewsView, SportNewsView, NewsEditView, NewsDeleteView, NewsCreateView, \
    admin_page_view, NewsSearchView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path('news/', news_list_view, name='news_list'),
    path('news/create', NewsCreateView.as_view(), name='news_creation'),
    path('news/<slug:news_slug>', news_detail_view, name='news_details'),
    path('news/<slug>/edit', NewsEditView.as_view(), name='news_edit'),
    path('news/<slug>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/', ContactPageView.as_view(), name="contact_page"),
    path("news/local/", LocalNewsView.as_view(), name='Mahalliy'),
    path("news/world/", WorldNewsView.as_view(), name='Xorij'),
    path("news/technology/", TechnologyNewsView.as_view(), name="Texnologiya"),
    path("news/sport/", SportNewsView.as_view(), name="Sport"),
    path("admins/", admin_page_view, name="admin_page"),
    path("search", NewsSearchView.as_view(), name="search_result")
]