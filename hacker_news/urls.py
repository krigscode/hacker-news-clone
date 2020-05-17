from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from links.views import UserProfileDetailView, UserProfileEditView

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('links.urls')),
    path('users/<slug>/', UserProfileDetailView.as_view(), name="profile"),
    path('edit_profile/', login_required(UserProfileEditView.as_view()), name="edit_profile"),
]
