"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
# from projects.views import ProjectDashboardView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=static('images/favicon.ico'))),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('dashboard/', include('projects.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Main application URLs
    path('projects/', include('projects.urls')),
    path('parts/', include('parts.urls', namespace='parts')),
    path('materials/', include('materials.urls', namespace='materials')),
    path('cutlists/', include('cutlists.urls')),
    path('shop-assets/', include('shop_assets.urls')),

    # Calculator application URLs
    path('calculators/', include('calculators.urls')),
    path('shelf/', include('shelf_calculator.urls')),
    path('wall-panels/', include('wall_panels.urls')),
    path('decking/', include('decking.urls')),
    path('golden-ratio/', include('golden_ratio.urls')),

    # Converter application URLs
    path('converters/', include('converters.urls', namespace='converters')),
    path('fraction-decimal-mm/', include('fraction_decimal_mm.urls')),

    # Reference application URLs
    path('references/', include('references.urls', namespace='references')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
