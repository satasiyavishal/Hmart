from django.conf import settings
from store_app.models import Order,OrderItem
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from store_app.models import Product,Color,Brand,Categories,Filter_Price,Contact_us,Tag
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
import razorpay


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


def BASE(request):
    return render(request,'Main/base.html')


def HOME(request):
    product = Product.objects.filter(status = 'Publish')

    context = {
        'product':product,
    }

    return render(request,'Main/index.html',context)


def PRODUCT(request):
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CAT_ID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_ID = request.GET.get('color')
    BRAND_ID = request.GET.get('brand')
    PRICE_LOWTOHIGH_ID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW_ID = request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCT_ID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCT_ID = request.GET.get('OLD_PRODUCT')


    if CAT_ID:
        product = Product.objects.filter(categories = CAT_ID,status = 'Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID,status = 'Publish')
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID,status = 'Publish')
    elif BRAND_ID:
        product = Product.objects.filter(brand = BRAND_ID,status = 'Publish')
    elif PRICE_LOWTOHIGH_ID:
        product = Product.objects.filter(status = 'Publish').order_by('price')
    elif PRICE_HIGHTOLOW_ID:
        product = Product.objects.filter(status = 'Publish').order_by('-price')
    elif NEW_PRODUCT_ID:
        product = Product.objects.filter(status = 'Publish',condition = 'New')
    elif OLD_PRODUCT_ID:
        product = Product.objects.filter(status = 'Publish',condition = 'Old')
    else:
        product = Product.objects.filter(status = 'Publish').order_by('-id')


    context = {
        'product':product,
        'categories':categories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand,
    }

    return render(request,'Main/product.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product':product
    }

    return render(request,'Main/search.html',context)


def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id = id).first()

    context = {
        'prod':prod
    }

    return render(request,'Main/single_product.html',context)


def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message,email_from, ['vishalsatasiya65@gmail.com'])
            contact.save()
            return redirect('home')
        except:
            return redirect('contact')

    return render(request,'Main/contact.html')


def ABOUT_PAGE(request):
    return render(request,'Main/about.html')


def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('login')
    

    return render(request,'Registration/auth.html')


def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')


    return render(request,'Registration/auth.html')


def HandleLogout(request):
    logout(request)
    
    return redirect('home')


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request,'Cart/cart_details.html')


def Check_out(request):
    payment = client.order.create({
        "amount": 500,
        "currency": "INR",
        "payment_capture": "1"
        })
    
    
    order_id = payment['id']
    context = {
       'order_id':order_id,
       'payment':payment,
    }
    return render(request,'Cart/checkout.html',context)


def Place_order(request):
    if request.method == "POST":
        uid = request.session.get('auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        # context = {
        #     'order_id':order_id
        # }

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']

            total = a * b

            item = OrderItem(
                user = user,
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()

    return render(request,'Cart/placeorder.html')
    

@csrf_exempt
def SUCCESS(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break

        user =  Order.objects.filter(payment_id = order_id).first()
        #user.paid = True
        #user.save()
    return render(request,'Cart/thank-you.html')


def Your_Order(request):
    uid = request.session.get('auth_user_id')
    user = User.objects.get(id = uid)

    order = OrderItem.objects.filter(user = user)
    context = {
        'order':order,
    }
    return render(request,'Main/your_order.html',context)

