from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from accounts.views import user_login, user_profile, user_register, edit_user

urlpatterns = [
    path("login/", LoginView.as_view(), name="login_page"),
    path("logout/", LogoutView.as_view(), name="logout_page"),
    path("my-profile/", user_profile, name="my_profile"),
    path("my-profile/password-change", PasswordChangeView.as_view(), name="password_change"),
    path("my-profile/password-change/done", PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("my-profile/password-reset", PasswordResetView.as_view(), name="password_reset"),
    path("my-profile/password-reset/done", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("my-profile/password-reset/<uidb64>/<token>", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("my-profile/password_reset/complete", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("my-profile/sign-up", user_register, name="signup_page"),
    path("my-profile/edit", edit_user, name="profile_edit")
]