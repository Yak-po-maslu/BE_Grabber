from django.http import HttpResponse


def index(request):
    return HttpResponse("Welkome in marketplace Grabber")

