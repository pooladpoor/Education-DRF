"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('todos/', include('todo.urls')),
    path('api-auth/', include('rest_framework.urls')), # برای  خود رست فریم ورک هست
    
    #################اهراز هویت 2####################
    # توش یوزر نیم و پسورد میزنی و توکن میسازه بهت میده که همیشه تو هد ریکوست بزاری
    path('auth-token/', obtain_auth_token, name='generate_auth_token'), # برای اهراز هویت با توکن

    #################اهراز هویت 3####################
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #####################سواگر (راهنما برای فرانت کار)########################
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
