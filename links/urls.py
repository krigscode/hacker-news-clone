from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from .views import LinkListView, signup, LinkCreateView, LinkDetailView, LinkUpdateView, LinkDeleteView, VoteFormView
from .views import add_comment_to_link, comment_approve, comment_remove
urlpatterns = [
    #======LINK_URLs======
    #CREATE 
    path('link/create/', login_required(LinkCreateView.as_view()), name="link_create"),
    #RETRIEVE
    path('', LinkListView.as_view(), name='home'), #list
    path('link/<pk>/', LinkDetailView.as_view(), name="link_detail"),
    #UPDATE
    path('link/<pk>/update/', login_required(LinkUpdateView.as_view()), name="link_update"),
    #DELETE
    path('link/<pk>/delete/', login_required(LinkDeleteView.as_view()), name="link_delete"),

    #======REGISTRATION_URLs======
    path('registration/login/', views.LoginView.as_view(), name='login'),
    path('registration/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/signup/', signup, name='signup'),
    #======VOTE_URLs======
    path('vote/', login_required(VoteFormView.as_view()), name="vote"),

    #======COMMENT_URLs======
    #CREATE
    path('link/<pk>/comment/', add_comment_to_link, name='add_comment_to_link'),
    #UPDATE
    path('comment/<pk>/approve/', comment_approve, name='comment_approve'),
    #DELETE
    path('comment/<pk>/remove/', comment_remove, name='comment_remove'),

]