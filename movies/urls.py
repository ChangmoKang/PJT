from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'movies'

urlpatterns = [
    path('', views.movie_index, name='movie_index'),
    path('suggestions/', views.movie_suggestions, name="movie_suggestions"),
    path('watchlist/', views.movie_watchlist, name="movie_watchlist"),
    
    
    path('get/', views.movie_get, name='movie_get'),
    path('get/genres/', views.genre_get, name='genre_get'),
    # path('get/<int:user_id>/watches/', views.watch_get, name='watch_get'),

    # path('<int:movie_id>/scores/create/', views.score_create, name='score_create'),
    # path('<int:movie_id>/scores/<int:score_id>/update/', views.score_update, name='score_update'),
    # path('<int:movie_id>/scores/<int:score_id>/delete/', views.score_delete, name='score_delete'),
    
    path('scores/', views.score_read_only, name='score_read_only'),
    path('<int:movie_id>/scores/', views.score_create_read, name='score_create_read'),
    path('scores/<int:score_id>/', views.score_update_delete, name='score_update_delete'),
    
]

# urlpatterns += [path('docs/', get_swagger_view(title="API Document"))]