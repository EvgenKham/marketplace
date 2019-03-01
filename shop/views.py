from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'categories': categories, 'products': products}
    return render(request, 'base.html', context)


def view_category(request, slug):
    cat_all = Category.objects.all()
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category_id=category.id)
    context = {'all': cat_all, 'category': category, 'products': products}
    return render(request, 'category.html', context)


def view_product(request, slug):
    cat_all = Category.objects.all()
    product = Product.objects.get(slug=slug)
    context = {'all': cat_all, 'product': product}
    return render(request, 'product_details.html', context)
