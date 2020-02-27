from django.urls import path
from rango import views
app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
   # path('category/<slug:artist_name_slug>/',
         #views.show_artist, name='show_artist'),
    #path('add_category/', views.add_artist, name='add_artist'),
    #path('category/<slug:artist_name_slug>/add_page/', views.add_review, name = 'add_review'),
    #path('register/', views.register, name='register'),
    #path('login/', views.user_login, name='login'),
    #path('restricted/', views.restricted, name='restricted'),
    #path('logout/', views.user_logout, name='logout'),

]
