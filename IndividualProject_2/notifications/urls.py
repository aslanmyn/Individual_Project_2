from django.urls import path
from .views import (
    NotificationListView,
    NotificationDetailView,
    NotificationTemplateListView
)

urlpatterns = [
    path('templates/', NotificationTemplateListView.as_view(), name='notification-template-list'),
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]