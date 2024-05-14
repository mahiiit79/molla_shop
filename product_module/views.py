from django.db.models import  Count
from django.http import  HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView,DetailView
from site_module.models import SiteBanner
from utils.convertors import group_list

from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from utils.http_service import get_client_ip






class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView,self).get_context_data()
        query = Product.objects.all()
        product : Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        return context


    def get_queryset(self):
        #'first this func then above func'
        query = super(ProductListView,self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = self.request.GET.get('start_price')
        end_price = self.request.GET.get('end_price')
        if start_price is not None:
            #Product.objects.filter(price__gte=start_price)gte yani >= gt mishe =
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        #Product.objects.filter(brand__url_title__exact=brand_name)baraye intelisance
        #iexact case sensetive nis vali exact hast

        if brand_name is not None :
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None :
            query = query.filter(category__url_title__iexact = category_name)
        return query

    # def get_queryset(self):
    #     base_query = super(ProductListView,self).get_queryset()
    #     data = base_query.filter(is_active=True)[:2]
    #     return data



class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position=SiteBanner.SiteBannerPositions.product_list)
        #context['product_galleries_group'] = ProductGallery.objects.filter(product_id=loaded_product).all()
        #'اگه مسخواشتم سه تا سه تا نمایش بده مثل صفحه ایندکس از گروپ لیست استفاده میکنم '
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0,loaded_product)
        context['product_galleries_group'] = group_list(galleries, 3)
        context['related_products'] = group_list(list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk = loaded_product.id).all()[:12]),3)
        #'exclude baes mishe khode mahsul ro neshun nade'





        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        #'میگه قبلش برو چک کن ببین بازدید داشته این کاربر یا نه '
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip,product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip,user_id=user_id,product_id=loaded_product.id)
            new_visit.save()


        return context



class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorite"] = product_id
        return redirect(product.get_absolute_url())

   # 'get quyery set ham mishe dasht'


# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         products = Product.objects.all().order_by('-price')[:2]
#         context = super(ProductListView,self).get_context_data()
#         context['products'] = products
#         return context

# def product_list(request):
#     products = Product.objects.all().order_by('-price')[:2]
#     return render(request, 'product_module/product_list.html', {
#         'products': products,
#     })






#
# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         slug = kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         context = super(ProductDetailView,self).get_context_data()
#         context['product'] = product



# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, 'product_module/product_detail.html', {
#         'product': product
#     })




def product_categories_component(request:HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True,is_delete=False)
    context = {
        'categories' : product_categories
    }
    return render(request,'product_module/components/product_component_categories.html',context)

def product_brands_component(request:HttpRequest):
    #'annotate()mige chizai k mikhay vakeshi kon ezafe ham miyaram barat'
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    #product_brands.product_set.count()'in khob nis chon miyad msln 100ta brand ro vakeshi mikone 100bar'
    context = {'brands':product_brands}
    return render(request,'product_module/components/product_brands_component.html',context)