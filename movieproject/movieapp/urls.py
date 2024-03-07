from . import views
from django.urls import path
from .views import add_movie, movie_detail, edit_movie, delete_movie,movie_list,category_movie_list
from django.contrib.auth import views as auth_views
app_name = 'movieapp'

urlpatterns = [
    # path('/', views.movie_home, name='home'),

    path('', views.movie_home, name='movie_home'),
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('list/', views.movie_list, name='movie-list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add/', views.add_movie, name='add_movie'),
    path('add-review/<int:movie_id>/', views.add_review, name='add_review'),
    # path('movie/<int:pk>/', movie_detail, name='movie_detail'),
    path('edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('<int:movie_id>/delete/', delete_movie, name='delete_movie'),
    # path('movies/', movie_list, name='movie_list'),
    path('mov/<movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movies, name='search_movies'),
    path('movies/category/<slug:category_slug>/', views.category_movie_list, name='category-movie-list'),
    
    

]