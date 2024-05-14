from article_module.models import Article, ArticleCategory, ArticleComment
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from jalali_date import date2jalali,datetime2jalali
from site_module.models import SiteBanner


# class ArticlesView(View):
#     def get(self,request):
#         articles = Article.objects.filter(is_active=True)
#         context = {'articles': articles}
#         return render(request,'article_module/articles_page.html',context)
#
#





class ArticlesListView(ListView):
    model = Article
    paginate_by = 1
    template_name = 'article_module/articles_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView,self).get_context_data(*args,**kwargs)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position=SiteBanner.SiteBannerPositions.product_list)
        return context

    #'این کد میاداونایی که دسته بندیشون با مقاله یکیه رو براساس ادرس میاره'
    def get_queryset(self):
        query = super(ArticlesListView,self).get_queryset()
        query = query.filter(is_active = True)
        category_name = self.kwargs.get('category')
        if category_name is not None :
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticleDetailView,self).get_queryset()
        query = query.filter(is_active = True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data()
        #'از طریق کد زیر به مقدار درون مدل مقاله دسترسی دارم'
        article : Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id,parent=None).order_by('-create_date').prefetch_related('articlecomment_set')
        #'prefetch_related('articlecomment_set)miyad ye query mizne javb c, ro miyare'
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context




#'این تابع برای دسته بندی های کنار صفحه مقالاته'
def articles_categories_component(request : HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,parent_id=None)
    context = {
        'article_main_categories':article_main_categories
    }
    return render(request,'article_module/components/article_categories_page.html',context)


# def add_article_comment(request: HttpRequest):
#     if request.user.is_authenticated:
#         article_id = request.GET.get('article_id')
#         article_comment = request.GET.get('article_comment')
#         parent_id = request.GET.get('parent_id')
#         print(article_id,article_comment,parent_id)
#         #'inja miyam az articlecomment ye sheye miszm va user_id be dalil inke goftim byd login bashe '
#         new_comment = ArticleComment(article_id=article_id,text=article_comment,user_id=request.user.id)
#         new_comment.save()
#         context = {
#             'comments' : ArticleComment.objects.filter(article_id=article_id,parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
#             'comments_count':ArticleComment.objects.filter(article_id=article_id).count()
#         }
#         return render(request,'article_module/includes/article_comment_partial.html',context)
#
#     print(request.GET)
#     return HttpResponse('response')

def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        print(article_id, article_comment, parent_id)
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }

        return render(request, 'article_module/includes/article_comment_partial.html', context)

    return HttpResponse('response')
