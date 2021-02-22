from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [
    path('posts', views.PostListView.as_view(), name='posts'),
    path('posts/new', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/update/<int:post_id>', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<int:post_id>', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/favorite', views.FavoriteView.as_view(), name='post_favorite'),
    path('posts/<int:post_id>/comments/new', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/comments/update/<int:comment_id>', views.CommentUpdateView.as_view(), name='comment_update'),
    path('posts/<int:post_id>/comments/delete/<int:comment_id>', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('posts/file-upload', views.UploadFileView.as_view(), name='file_upload'),
]
