from django.urls import path, include
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_movie/', views.create_movie, name='create_movie'),
    path('<int:movie_id>/', views.detail_movie, name='detail_movie'),
    path('<int:movie_id>/create_review/', views.create_review, name='create_review'),
    path('<int:review_id>/detail_review/', views.detail_review, name='detail_review'),
    path('<int:review_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:review_id>/delete_review/', views.delete_review, name='delete_review'),
    path('<int:review_id>/like_review/', views.like_review, name='like_review'),

    # path('')
]
