from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.views.generic.list import ListView

from users.models import Profile
from shop.models import Category, Product
from cart.models import Cart
from cart.forms import CartAddProductForm
from orders.models import OrderItem, Order


@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:CartDetail')


def cart_remove(request, product_id):
    """Удалить товар из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')


def cart_detail(request):
    """Просмотр корзины заказов"""
    cart = Cart(request)
    cat_all = Category.objects.all()
    user = Profile.objects.get(user=request.user)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})

    return render(request, 'cart_detail.html', {'cart': cart, 'cat_all': cat_all, 'user': user})


# class OrdersDetail(ListView):
#     model = OrderItem
#     context_object_name = 'my_orders'
#
#     def get_queryset(self):
#         result = OrderItem.objects.filter(sess_id=self.request.session.session_key)
#         if len(result) < 1:
#             result = 'no orders'
#         return result
#         pass
#
#     def get_template_names(self):
#         return ['current_orders.html']
#         pass
