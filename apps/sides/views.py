from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from .models import Comment, Favorite, Score
from apps.products.models import Product
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from utils import page_path, partial_path
from django.db.models import Q



appname = 'sides'
# ===================================== Partials ========================================

class CreateCommentView(View):
    template_name = partial_path(appname, 'create_comment')
    
    def get(self, request, **kwargs):
        product_id = request.GET.get('productId')
        comment_id = request.GET.get('commentId')
        slug = kwargs.get('slug')
        initial_dict = {
            'product_id': product_id,
            'comment_id': comment_id
        }
        form = CommentForm(initial=initial_dict)
        return render(request, self.template_name, {'form': form, 'slug': slug})
    
    def post(self, request, **kwargs):
        slug = kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data['comment_id']
            comment_text = form.cleaned_data['comment_text']
            reply_to = None
            if comment_id:
                reply_to_id = comment_id
                reply_to = get_object_or_404(Comment, id=reply_to_id)
            Comment.objects.create(
                user = request.user,
                product = product,
                text = comment_text,
                reply_to = reply_to
            )
            messages.success(request, 'نظر شما ثبت شد', 'success')
            return redirect('products:product', slug)
        messages.error(request, 'خطا در ارسال نظر', 'danger')
        return redirect('products:product', slug)
    
def favorites_detail(request):
    favorites = request.user.favorites.all()
    return render(request, partial_path(appname, 'favorites_detail'), {'favorites': favorites})


# ===================================== Pages ========================================

class FavoriteView(TemplateView):
    template_name = page_path(appname, 'favorites')


class SearchView(TemplateView):
    template_name = page_path(appname, 'search')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(text__icontains = query)
        )
        context['products'] = products
        return context
        

# ===================================== Ajax ========================================

def add_score(request):
    product_id = request.GET.get('productId')
    score = request.GET.get('score')
    product = get_object_or_404(Product, id=product_id)
    Score.objects.create(
        product = product, 
        score = score,
        user = request.user
        )
    avg = product.get_avg_score()
    return HttpResponse(avg)


def add_to_favorites(request):
    product_id = request.GET.get('productId')
    product = get_object_or_404(Product, id=product_id)
    flag = Favorite.objects.filter(product=product, user=request.user).exists()
    if not flag:
        Favorite.objects.create(user=request.user, product=product)
        return HttpResponse()
    return HttpResponse()

def favorites_status(request):
    user_favorites = request.user.favorites.all()
    return HttpResponse(user_favorites.count())

def delete_from_favorites(request):
    product_id = request.GET.get('product_id')
    user_favorites = request.user.favorites.filter(product_id=product_id)
    user_favorites.delete()
    return redirect('sides:favorites_detail')

