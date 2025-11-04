from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='api/v1.0/', permanent=False)),
    path('api/v1.0/', include('api.urls'), name='api-endpoint'),
    path('service/admin/', admin.site.urls),
]
