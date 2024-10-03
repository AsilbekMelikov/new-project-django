from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import News, Category
from .forms import ContactForms, CommentForm
from news_project.custom_permission import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.


def news_list_view(request):
    news_list = News.published.all()

    context = {
        'news_lists': news_list
    }

    return render(request, 'news/news_list.html', context)

def news_detail_view(request, news_slug):
    details = News.objects.get(slug=news_slug)
    comments = details.comments.filter(active=True)
    new_comment = None
    hit_context = {}
    hit_count = get_hitcount_model().objects.get_for_object(details)
    hits = hit_count.hits
    hit_context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits += 1
        hit_context['hit_counted']  = hit_count_response.hit_counted
        hit_context['hit_message'] = hit_count_response.hit_message
        hit_context['total_hits'] = hits

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, )
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news_id = details.id
            new_comment.user = request.user
            new_comment.save()

            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "detail": details,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form
    }
    context.update(hit_context)
    print(context)
    return render(request, 'news/news_details.html', context)

# def home_page_view(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by("-publish_time")[:10]
#     local_news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:6]
#
#     context = {
#         "news_list": news_list,
#         "categories": categories,
#         "latest_local_news":local_news[0],
#         "local_news": local_news[1:]
#     }
#     return render(request, "news/home.html", context)

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

class NewsEditView(OnlyLoggedSuperUser, UpdateView):
    template_name = "crud/news_edit.html"
    model = News
    fields = ["title", "body", "image", "category", "status"]

    def get_success_url(self):
        return reverse_lazy('news_details', kwargs={'news_slug': self.object.slug})


class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    template_name = "crud/news_delete.html"
    model = News
    success_url = reverse_lazy("home_page")

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    template_name = "crud/news_create.html"
    model = News
    fields = ["title", "slug", "body", "image", "category", "status"]
    success_url = reverse_lazy("home_page")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["slug"].help_text = "<p>Slug can be empty because it takes title If you want another, enter a unique identifier</p>"
        return form

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url=None)
def admin_page_view(request):
    admins = User.objects.all().filter(is_superuser=True)

    if not request.user.is_superuser:
        return HttpResponseForbidden("<h1>You are not allowed to this page</h1>")

    context = {
        "admins": admins
    }
    return render(request, "pages/admins_page.html", context)

class NewsSearchView(ListView):
    template_name = "news/search_result.html"
    model = News
    context_object_name = "search_result"


    def get_queryset(self):
        query = self.request.GET.get("q")
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))























