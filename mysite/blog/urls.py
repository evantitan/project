from django.urls import path
from .import views

app_name = 'blog'

urlpatterns = [
    path('search/',views.post_search, name='post_search'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail, name='post_detail'),
    path('<int:id>/save/',views.bookmark_post, name='bookmark_post'),
    path('bookmarks/',views.bookmark, name='bookmark'),
    path('delete/<int:id>',views.delete_bookmark, name='delete_bookmark'),
    path('<int:id>/post_comment/',views.post_comment, name='post_comment'),
    path('tag/<slug:tag_name>/',views.post_list_by_tag, name='post_list_by_tag'),
    path('learn/',views.learn, name='learn'),
    path('<int:post_id>/share/',views.share_by_email, name='share_by_email'),
    path('comming-soon/',views.comming_soon, name='comming_soon'),
]
