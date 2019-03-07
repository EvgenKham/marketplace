from django.shortcuts import render, redirect
from .models import OrderItem, Order
from cart.models import Cart
from users.models import Profile
from shop.models import Product


def buy_product(request):
    user = request.user
    cart = Cart(request)
    """Если в корзине есть товары, то приобретаем их"""
    if cart.item_count() != 0:
        """Создание заказа"""
        Order.objects.create(customer=user.username)
        order = Order.objects.filter(customer=user.profile).latest('created')
        """У покупателя списываются средства со счета"""
        sum_buy = float(user.profile.account) - cart.get_total_price()
        Profile.objects.filter(user_id=user.id).update(account=sum_buy)

        for item in cart:
            """Определение суммы товара, продоваемого продукта, продавца"""
            sum_one_product = float(item['price']) * float(item['quantity'])
            product_sold = Product.objects.get(name=item['product'])
            seller = Profile.objects.get(id=product_sold.owner.id)
            """Зачисление средств на счет продавца"""
            old_account = seller.account
            new_account = float(old_account) + float(sum_one_product)
            Profile.objects.filter(id=seller.id).update(account=new_account)
            """Создание единицы заказанного товара из корзины"""
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'],
                                     )
        cart.clear()
        return render(request, 'thanks.html', {'order': order})
    else:
        return redirect('/')
