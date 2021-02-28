from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('network/', include('accounts.urls'))
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]


