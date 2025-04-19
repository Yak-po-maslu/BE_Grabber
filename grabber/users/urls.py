from django.urls import path


from .views import AsyncCookieView

urlpatterns = [
    path('login/', AsyncCookieView.login, name='login'),
    path('register/', AsyncCookieView.register, name='register'),
]
