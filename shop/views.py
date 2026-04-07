from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order

def home(request):
    category = request.GET.get('category')
    query = request.GET.get('q')

    products = Product.objects.all()

    if category:
        products = products.filter(category__iexact=category)

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'shop/home.html', {'products': products})


def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        name = request.POST.get('customer_name')
        quantity = int(request.POST.get('quantity', 1))
        Order.objects.create(product=product, customer_name=name, quantity=quantity)
        return redirect('home')

    return render(request, 'shop/order.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart
    return redirect('home')


def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        product.qty = qty
        product.total_price = product.price * qty
        total += product.total_price
        products.append(product)

    return render(request, 'shop/cart.html', {'products': products, 'total': total})