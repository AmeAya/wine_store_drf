"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('country', CountryApiView.as_view()),  # http://127.0.0.1:8000/country
    # path('type_wine', WineByTypeApiView.as_view()),
    path('wine_filter', WineFilterApiView.as_view()),
    path('auth', AuthApiView.as_view()),
    path('reg', RegistrationApiView.as_view()),
    path('cab', UserCabinetApiView.as_view()),
    path('meal', MealApiView.as_view()),
    path('search', WineSearchApiView.as_view()),
    path('paginator', WinePaginatedApiView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
