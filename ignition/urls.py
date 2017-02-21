from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
import matching
from matching import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('matching.urls')),
]
