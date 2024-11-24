from django.urls import path
from .views import GradeListCreateView, GradeDetailView

urlpatterns = [
    path('', GradeListCreateView.as_view(), name='grade-list-create'),
    path('<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),
]