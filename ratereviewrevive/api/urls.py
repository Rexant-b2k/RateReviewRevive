from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
                views.CommentViewSet,
                'comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet,
                'reviews')
router.register(r'categories', views.CategoryViewSet, 'categories')
router.register(r'genres', views.GenreViewSet, 'genres')
router.register(r'titles', views.TitleViewSet, 'titles')
router.register('users', views.UserViewSet, 'users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.create_user, name='signup'),
    path('v1/auth/token/', views.check_token, name='check_token')
]
