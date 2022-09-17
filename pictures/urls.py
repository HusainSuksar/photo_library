from django.urls import re_path as url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pictures'

urlpatterns = [
    url(r'^login/', views.loginPage, name='login'),
    url(r'^logout/', views.logoutPage, name='logout'),

    url(r'^$', views.index, name='index'),
    url(r'^search/', views.search_results, name='search'),
    url(r'^location/(?P<location>\w+)/', views.image_location, name='location'),
    url(r'^add/', views.addPhoto, name='add'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
