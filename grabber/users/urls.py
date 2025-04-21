from django.urls import path


from .views import AsyncCookieViewLogin, AsyncCookieViewRegister

urlpatterns = [
    path('login/', AsyncCookieViewLogin.as_view(), name='login'),
    path('register/', AsyncCookieViewRegister.as_view() , name='register'),
]
