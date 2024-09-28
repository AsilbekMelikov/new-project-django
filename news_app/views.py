from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import News, Category
from .forms import ContactForms


# Create your views here.


def news_list_view(request):
    news_list = News.published.all()

    context = {
        'news_lists': news_list
    }

    return render(request, 'news/news_list.html', context)

def news_detail_view(request, news_slug):
    details = News.objects.get(slug=news_slug)

    context = {
        'detail': details
    }
    return render(request, 'news/news_details.html', context)

def home_page_view(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by("-publish_time")[:10]
    local_news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:6]

    context = {
        "news_list": news_list,
        "categories": categories,
        "latest_local_news":local_news[0],
        "local_news": local_news[1:]
    }
    return render(request, "news/home.html", context)

class HomePageView(ListView):
    template_name = "news/home.html"
    model = Category
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_list"] = News.published.all().order_by("-publish_time")[:10]
        context["categories"] = Category.objects.all()
        context["local_news"] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:5]
        context["world_news"] = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[:5]
        context["technology_news"] = News.published.all().filter(category__name="Texnologiya").order_by("-publish_time")[:5]
        context["sport_news"] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[:5]
        return context


# def contact_page_view(request):
#     form = ContactForms(request.POST)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langaningiz uchun rahmat</h2>")
#
#     context = {
#         "form": form
#     }
#     return render(request, "news/contact.html", context)

class ContactPageView(TemplateView):
    template_name = "news/contact.html"

    def get(self, request, *args, **kwargs):
        form = ContactForms()
        context = {
            "form": form
        }
        return render(request, "news/contact.html", context)

    def post(self, request, *args, **kwargs):
        form = ContactForms(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> Hammasi ajoyib")
        context = {
            "form": form
        }
        return render(request, "news/contact.html", context)

class LocalNewsView(ListView):
    template_name = "pages/local_news.html"
    model = News
    context_object_name = "local_news"

    def get_queryset(self):
        local_news = self.model.published.all().filter(category__name="Mahalliy")
        return local_news

class WorldNewsView(ListView):
    template_name = "pages/world_news.html"
    model = News
    context_object_name = "world_news"

    def get_queryset(self):
        world_news = self.model.published.all().filter(category__name="Xorij")
        return world_news

class TechnologyNewsView(ListView):
    template_name = "pages/technology_news.html"
    model = News
    context_object_name = "technology_news"

    def get_queryset(self):
        technology_news = self.model.published.all().filter(category__name="Texnologiya")
        return technology_news


class SportNewsView(ListView):
    template_name = "pages/sport_news.html"
    model = News
    context_object_name = "sport_news"

    def get_queryset(self):
        sport_news = self.model.published.all().filter(category__name="Sport")
        return sport_news