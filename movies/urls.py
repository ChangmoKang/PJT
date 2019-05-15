from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'movies'

urlpatterns = [
    path('', views.movie_index, name='movie_index'),
    path('get/', views.movie_get, name='movie_get'),
    path('get/genres/', views.genre_get, name='genre_get'),
    path('get/nations/', views.nation_get, name='nation_get'),
    path('get/directors/', views.director_get, name='director_get'),
    path('get/actors/', views.actor_get, name='actor_get'),
    path('get/stillCuts/', views.stillCut_get, name='stillCut_get'),
    
    path('<int:movie_id>/scores/create', views.score_create, name='score_create'),
    path('<int:movie_id>/scores/<int:score_id>/update/', views.score_update, name='score_update'),
    path('<int:movie_id>/scores/<int:score_id>/delete/', views.score_delete, name='score_delete'),
    # path('<int:movie_id>/scores/', views.score_create_read, name='score_create_read'),
    # path('<int:movie_id>/scores/<int:score_id>/', views.score_update_delete, name='score_update_delete'),
    path('suggestions/', views.movie_suggestions, name="movie_suggestions"),
]

# urlpatterns += [path('docs/', get_swagger_view(title="API Document"))]