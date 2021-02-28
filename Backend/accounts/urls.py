from django.urls import path
from .views import ScrapView, GetCSRFToken,FilterView


urlpatterns = [
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('scrap/', ScrapView.as_view()),
    path('filter/', FilterView.as_view())
]