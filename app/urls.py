from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import user_profile,signup, profile,searchuser,follow,unfollow, comment


urlpatterns = [

    path('', views.welcome , name='index'),
    path('comments/<int:id>', comment, name='comments'),
    path('new/image/', views.upload_image, name='new-image'),
    path('signup/', signup , name='signup'),
    path('user_profile/<username>/', user_profile, name='user_profile'),
    path('profile/', profile, name='profile'),
    path('search/',views.searchuser ,name='searchuser'),
    path('follow/<pk>', follow, name='follow'),
    path('unfollow/<pk>',unfollow, name='unfollow'),
    
	

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)