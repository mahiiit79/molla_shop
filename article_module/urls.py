from django.urls import path
from .views import ArticlesListView,ArticleDetailView,add_article_comment

urlpatterns = [
    path('',ArticlesListView.as_view(),name='articles_list'),
    path('cat/<str:category>', ArticlesListView.as_view(), name='articles_by_category_list'),
    path('<pk>/', ArticleDetailView.as_view(), name='articles_detail_page'),
    path('add-article-comment', add_article_comment, name='add_article_comment')

]

