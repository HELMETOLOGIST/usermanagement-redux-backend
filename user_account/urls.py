from django.urls import path
from .views import RegisterView, RetrieveUpdateDeleteUserView, ListUsersView, UserProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/<int:pk>/', RetrieveUpdateDeleteUserView.as_view(), name='retrieve_update_delete_user'),
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),  # New URL pattern
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)