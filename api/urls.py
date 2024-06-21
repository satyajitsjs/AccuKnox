from django.urls import path
from api import views as v

urlpatterns = [
    path('register/', v.register_user , name='register'),
    path('login/', v.login_user , name='login'),
    path('get_access_token/', v.get_access_token , name='get-access-token'),
    path('search/', v.user_search, name='search'),
    path('friend-request/', v.send_friend_request, name='friend-request'),
    path('friend-request/respond/', v.respond_friend_request, name='respond-friend-request'),
    path('friends/', v.list_friends, name='friends'),
    path('pending-requests/', v.list_pending_requests, name='pending-requests'),


]
