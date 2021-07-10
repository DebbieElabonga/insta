from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import user_profile,signup, welcome


urlpatterns = [

    path('', views.welcome , name='index'),
    path(r'comments/<id>', views.comment, name='comments'),
    path(r'user_profile/<username>', user_profile, name='user_profile'),
    path('new/image/', views.upload_image, name='new-image'),
    path('signup/', signup , name='signup'),
	

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)