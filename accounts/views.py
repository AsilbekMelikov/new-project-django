from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.contrib import messages

from accounts.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile


# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Login has been successful")
                else:
                    return HttpResponse("User is not active")
            else:
                return HttpResponse("User not found")
    else:
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "registration/login.html", context)

@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.all().get(user=user)
    context = {
        "user": user,
        "profile": profile
    }
    return render(request, "pages/my_profile.html", context)

def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user": new_user
            }
            return render(request, "registration/signup_done.html", context)
        else:
            return HttpResponse("Your form is not valid")
    else:
        user_form = UserRegistrationForm()
        context = {
            "form": user_form
        }
        return render(request, "registration/signup.html", context)

# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login_page")
#     template_name = "registration/signup.html"
#
# class SignUpView2(View):
#
#    def get(self, request):
#        pass
#
#    def post(self, request):
#        pass


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully")

            return redirect("my_profile")

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            "user_form": user_form,
            "profile_form":profile_form
        }
        return render(request, "registration/profile_edit.html", context)













