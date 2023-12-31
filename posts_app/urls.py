from django.urls import path
from .views import pre_search, PostsView, PostsViewSet, SearchViewSet, get_categories, delete_file
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'search',SearchViewSet, basename='search')


urlpatterns = [
    path('<int:_id>/', PostsView.as_view()),
    path('', PostsView.as_view()),
    # path('posts/all/', all_posts.as_view()),
    # path('posts/create', post),
    # path('posts/search', search),
    path('pre-search', pre_search),
    path('get-categories/', get_categories),
    path('allposts/', PostsViewSet.as_view(), name='allposts'),
    path('delete-file/<int:id>/', delete_file)
    # path('upload/', ImageUploadView.as_view(), name='image-upload'),
]

urlpatterns += router.urls