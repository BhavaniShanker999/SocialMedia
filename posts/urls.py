
from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts',AddPosts,basename="getandcreateposts")
router.register(r'like',LikeDislikePosts,basename="like_dislike")
router.register(r'getpostdetails',GetPosts,basename="getpostdetails")
router.register(r'getlistoflikedusers',GetListOfLikedUsers,basename="getlistoflikedusers")


urlpatterns = [
    path('',include(router.urls)),
    
    ]
