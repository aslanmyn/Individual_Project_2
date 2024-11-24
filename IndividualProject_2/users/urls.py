from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestUserView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('test/', TestUserView.as_view(), name='test-user'), 
] + router.urls  