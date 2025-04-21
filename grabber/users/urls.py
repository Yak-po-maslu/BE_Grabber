from django.urls import path
from .views import (
    AsyncCookieViewLogin,
    AsyncCookieViewRegister,
    AsyncCookieViewRefresh,
    AsyncCookieViewLogout,
)

urlpatterns = [
    path('login/', AsyncCookieViewLogin.as_view(), name='login'),
    path('register/', AsyncCookieViewRegister.as_view() , name='register'),
    path('refresh/', AsyncCookieViewRefresh.as_view(), name='refresh'),
    path('logout/', AsyncCookieViewLogout.as_view(), name='logout'),
]
