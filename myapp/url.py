from django.conf import settings
from django.conf.urls import static
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('users/register/', views.CreateUserView.as_view(), name="register"),
    path('account/login-gmail', views.LoginWithGmail.as_view(), name="login-gmail"),
    path('account/user', views.UpdateUser.as_view(), name="register"),
    path('account/upload-pp/<int:id>', views.UserProfilePictureUpload.as_view(), name="upload-user-pp"),
    path('account/upload-profile/<int:id>', views.uploadUserProfile, name="upload-profile"),
    path('account/user/<int:id>', views.CurrentUser.as_view()),
    path('account/users', views.Users.as_view()),
    path('user-details', views.UserDetail.as_view()),
    path('search-event', views.searchEvent.as_view()),
    path('events-g', views.GlobalEvents.as_view()),
    path('event', views.Events.as_view()),
    path('events', views.EventList.as_view()),
    path('event/<int:id>', views.Events.as_view()),
    path('event/uploadImg/<int:id>', views.UploadEventImage.as_view()),
    path('event/test-upload/<int:id>', views.testUpload.as_view()),
    path('search', views.SearchList.as_view()), 
    path('get-ticket/<int:id>', views.getTicket.as_view()),
    path('adgenda', views.CreateAdgena.as_view()),
    path('sort-adgenda', views.SortAdgenda.as_view()),
    path('adgenda/<int:id>', views.AdgendaAPI.as_view()),
    path('suggest-adj-invite', views.Connections.as_view()),
    path('add-market-place', views.MarketPlaceAPIView.as_view()),
    path('market-place/<int:id>', views.MarketPlaceAPIView.as_view()),
    path('list-market-places', views.MarketPlaceList.as_view()),
    path('market-places-g', views.GlobalMarketPlaceList.as_view()),
    path('search-market-palce', views.SearchMarketPlace.as_view()),
    path('invite-connections', views.InviteConnections.as_view()),
    path('market-place-pictures/<int:id>', views.MarketPlaceUploadPicture.as_view()),
    path('invite-connections/<int:id>', views.getAgendaConnection.as_view()),
    path('upload-image/<int:id>', views.UserProfilePictureUpload.as_view(), name='upload-image'),
    # path('event-image', views.UserProfilePictureUpload.as_view(), name='upload-image')
    path('canlendar', views.Calendar.as_view(), name='calendar'),
    path('count-records', views.Records.as_view(), name='records')
]
