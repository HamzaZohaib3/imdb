from django.contrib import admin
from django.urls import path
from imbd_api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"stream", views.streamplatformViewSet, basename="streamplatform")
router.register(r"watch", views.watchlistViewSet, basename="watchlist")


urlpatterns = [

    path("",views.api_root), 
    path("", include(router.urls)),

] 
