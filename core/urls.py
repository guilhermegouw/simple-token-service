from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/companies/", include("companies.urls")),
    path('api/tokens/', include('tokens.urls')),
]
