from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'movies'

urlpatterns = [
    path('', views.movie_index, name='movie_index'),
    path('<int:movie_id>/scores/', views.score_create_read, name='score_create_read'),
    path('<int:movie_id>/scores/<int:score_id>/', views.score_update_delete, name='score_update_delete'),
]

urlpatterns += [path('docs/', get_swagger_view(title="API Document"))]