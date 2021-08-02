"""warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from adminstore import views as adminview

urlpatterns = [
    path('', include('adminstore.urls')),
    path('login', adminview.login_system, name="login"),
    path('recovery', adminview.recovery, name="recovery"),
    path('profile-password', adminview.changePassword, name="profile_password"),
    path('profile', adminview.profile, name="profile"),
    path('forgot', adminview.forgot, name="forgot"),
    path('reset-password-confirmation/<str:uidb64>/<str:token>/', adminview.reset_password, name='password_reset_confirm'),
    path('logout', adminview.logout_system, name="logout"),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

handler404 = adminview.handler404
handler500 = adminview.handler500

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)