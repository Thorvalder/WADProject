from django.urls import path
from INKLined_app import views
app_name = 'INKLined_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    path('my-account/', views.show_account, name='show_account'),
    path('my-account/delete-account/', views.delete_account, name='delete_account'),
    path('my-account/saved-artists/', views.show_saved, name='show_saved'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-up/customer-sign-up/', views.register_customer, name='add_customer'),
    path('sign-up/artist-sign-up/', views.register_artist, name='add_artist'),
    path('artists/', views.artists, name='artists'),
    path('artists/<ARTIST_USERNAME>/', views.show_artist, name='show_artist'),
    path('artists/<ARTIST_USERNAME>/reviews/', views.show_reviews, name='show_reviews'),
    path('artists/<ARTIST_USERNAME>/reviews/add-a-review/', views.add_review, name='add_review'),
    path('logout/', views.user_logout, name='logout'),
    path('artists/<ARTIST_USERNAME>/save-artist/', views.save_artist, name='save_artist'),
    path('my-account/add-picture/', views.add_picture, name='add-picture'),

]
