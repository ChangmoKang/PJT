from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'movies'

urlpatterns = [
    path('', views.movie_index, name='movie_index'),
    path('<int:movie_id>/scores/create', views.score_create, name='score_create'),
    path('<int:movie_id>/scores/<int:score_id>/update/', views.score_update, name='score_update'),
    path('<int:movie_id>/scores/<int:score_id>/delete/', views.score_delete, name='score_delete'),
]

# urlpatterns += [path('docs/', get_swagger_view(title="API Document"))]