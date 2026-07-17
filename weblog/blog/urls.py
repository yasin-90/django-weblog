from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('tag/<int:tag_id>/', views.tag_posts, name='tag_posts'),
]