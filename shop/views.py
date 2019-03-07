from django.shortcuts import render, redirect
from shop.models import Category, Product
from shop.forms import CreateProductForm
from users.models import Profile
from cart.models import Cart
from cart.forms import CartAddProductForm


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    phones = Product.objects.filter(category__name="Телефоны")
    cart = Cart(request)
    context = {'categories': categories,
               'products': products,
               'phones': phones,
               'cart': cart}
    return render(request, 'base.html', context)


def view_category(request, slug):
    cat_all = Category.objects.all()
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category_id=category.id)
    cart = Cart(request)
    context = {'cat_all': cat_all,
               'category': category,
               'products': products,
               'cart': cart}
    return render(request, 'category.html', context)


def view_product(request, slug):
    cat_all = Category.objects.all()
    product = Product.objects.get(slug=slug)
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    context = {'cat_all': cat_all,
               'product': product,
               'cart_product_form': cart_product_form,
               'cart': cart}
    return render(request, 'product_details.html', context)


def add_product(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = Profile.objects.get(user=request.user)
            """Если картинку передали, то она устанавливается как icon для product,
            иначе устанавливается значение по умолчанию"""
            image = request.FILES.get('icon')
            if image:
                product.icon = image
            product.save()
            return redirect('/user/account/')
        return render(request, 'add_product.html', {'form': form, 'cart': cart})
    else:
        form = CreateProductForm()
        return render(request, 'add_product.html', {'form': form, 'cart': cart})
