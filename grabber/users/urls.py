from django.urls import path
from django.urls import path
from .views import (
    AsyncCookieViewLogin,
    AsyncCookieViewRegister,
    AsyncCookieViewRefresh,
    AsyncCookieViewLogout,
    UserProfileView,
)

app_name = 'users'  # дозволяє використовувати простір імен при реверсі

urlpatterns = [
    # 🔐 Auth endpoints
    path('login/', AsyncCookieViewLogin.as_view(), name='login'),
    path('register/', AsyncCookieViewRegister.as_view(), name='register'),
    path('refresh/', AsyncCookieViewRefresh.as_view(), name='refresh'),
    path('logout/', AsyncCookieViewLogout.as_view(), name='logout'),

    # 👤 User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
]
