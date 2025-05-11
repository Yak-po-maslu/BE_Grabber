
from django.urls import path
from .views import (
    login,
    register,
    refresh,
    logout,
    user_profile,
    forgot_password,
    reset_password,
    delete,
    add_image_profile
)

app_name = 'users'  # дозволяє використовувати простір імен при реверсі

urlpatterns = [
    # 🔐 Auth endpoints
    path('login/', login.AsyncCookieViewLogin.as_view(), name='login'),
    path('register/', register.AsyncCookieViewRegister.as_view(), name='register'),
    path('refresh/', refresh.AsyncCookieViewRefresh.as_view(), name='refresh'),
    path('logout/', logout.AsyncCookieViewLogout.as_view(), name='logout'),

    # 👤 User profile
    path('profile/', user_profile.AsyncUserProfileView.as_view(), name='profile'),

    path('forgot-password/', forgot_password.AsyncForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', reset_password.AsyncResetPasswordView.as_view(), name='reset-password'),
    path('delete/', delete.AsyncDeleteUserView.as_view(),name='delete_user'),
    path('upload-profile-image/',add_image_profile.AddImageProfileView.as_view(),name='add_image_profile'),
]
