from django.contrib import admin
from django.urls import path
from imbd_api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"stream", views.streamplatformViewSet, basename="streamplatform")


urlpatterns = [
    path("list/",views.movie_list,name = "movie_list"),
    path("list/<int:pk>/",views.movie_detail,name = "movie_details"),
    path("", include(router.urls)),
    path("",views.api_root),
    
] 
# urlpatterns = format_suffix_patterns(urlpatterns)