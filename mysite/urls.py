"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from trips.views import welcome,questionnaire,questionnaire02,questionnaire03,questionnaire04,questionnaire05,questionnaire06,questionnaire07,questionnaire08,questionnaire09,questionnaire10	
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', welcome),
    url(r'^result$',questionnaire),
    url(r'^result02$',questionnaire02),
    url(r'^result03$',questionnaire03),
    url(r'^result04$',questionnaire04),
    url(r'^result05$',questionnaire05),
    url(r'^result06$',questionnaire06),
    url(r'^result07$',questionnaire07),
    url(r'^result08$',questionnaire08),
    url(r'^result09$',questionnaire09),
    url(r'^result10$',questionnaire10)

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
