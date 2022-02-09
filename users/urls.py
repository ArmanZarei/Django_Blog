from django import views
from django.urls import path
from . import views
from .views import ProfileListView, FollowingView

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profiles-list'),
    path('profile/<int:pk>/follow', FollowingView.as_view(), name='follow-profile'),
]
