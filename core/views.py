from django.shortcuts import render, redirect, get_object_or_404
from .models import Items,OrderItem, Order, Address
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.core.serializers import serialize
from .form import address_form
from django.contrib import messages

def item_list(request):
    items_list = Items.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(items_list, 2)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = Paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {
        'items': items
    }
    return render(request, 'home.html', context)


def checkout(request):
    if request.method == 'POST':
        form = address_form(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            use_for_next_time = form.cleaned_data.get('use_for_next_time')
            payment_method = form.cleaned_data.get('payment_method')
            if use_for_next_time:
                default = True
                address, created = Address.objects.update_or_create(
                user = request.user,
                default_address = default,
                defaults = {
                'email' : email,
                'country' : country,
                'address' : address,
                'zip' : zip,
                'payment_method' : payment_method})
                order = Order.objects.filter(
                    user = request.user,
                    ordered = False
                ).first()
                order.address = address
                order.save()
                context = {
                    'order': order
                }
                return render (request, 'order-done.html', context)
            else: 
                default = False
                address =  Address(
                user = request.user,
                email = email,
                country = country,
                address = address,
                zip = zip,
                default_address = default,
                payment_method = payment_method
                )
                address.save()
                order = Order.objects.filter(
                    user = request.user,
                    ordered = False
                ).first()
                order.address = address
                order.save()
                context = {
                    'order': order
                }
                return render (request, 'order-done.html', context)
        else:
            print('not')
            print (form.errors)
            return render(request, 'checkout.html', {'form': form})
    else:
        form = address_form()
        default_address = Address.objects.filter(
            user = request.user,
            default_address = True
        ).first()
        if default_address:
            form.fields['email'].initial = default_address.email
            form.fields['country'].initial = default_address.country
            form.fields['zip'].initial = default_address.zip
            form.fields['address'].initial = default_address.address
        return render(request, 'checkout.html', {'form': form})

def product(request, pk):
    context = {
        'item': Items.objects.get(pk = pk)
    }
    return render(request, 'product.html', context)

def add_to_cart(request, pk):
    item = get_object_or_404(Items, pk = pk)
    order_item, created = OrderItem.objects.get_or_create(
        user = request.user,
        item = item,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        print(serialize('json', order_qs))
        if order.items.filter(item__id = item.id).exists():
            order_item.quantity += 1
            order_item.save()
            print('exists')
            return redirect("core:product", pk = pk)
        else:
            order.items.add(order_item)
            return redirect("core:product", pk = pk)

        return redirect("core:product", pk = pk)
    else:
        order_date = timezone.now()
        order = Order.objects.create(
            ordered_date = order_date,
            user = request.user,
            ordered = False
        )
        order.items.add(order_item)
        return redirect("core:product", pk = pk)


def remove_from_cart(request, pk):
    item = get_object_or_404(Items, pk = pk)
    order_qs =Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            order_item = OrderItem.objects.filter(
                user = request.user,
                item = item,
                ordered = False
            )[0]
            print(order)
            order.items.remove(order_item)
            order_item.delete()
            if not order.items.count():
                order_qs.delete()
            return redirect("core:product", pk = pk)
        else:
            print('does not exists')
            return redirect("core:product", pk = pk)
    else:
        print('does not exists Order')
        return redirect("core:product", pk = pk)

def order_summary(request):
    order = Order.objects.get(user= request.user, ordered = False)
    context = {
        'order' : order
    }
    return render(request, 'order-summry.html', context)

def add_single_item(request, pk):
    item = get_object_or_404(Items, pk = pk)
    order_item = OrderItem.objects.get(
        user = request.user,
        item = item,
        ordered = False
    )
    order_item.quantity += 1
    order_item.save()
    return redirect('core:order-summary')

def remove_single_item(request, pk):
    item = get_object_or_404(Items, pk = pk)
    order_item = OrderItem.objects.get(
        user = request.user,
        item = item,
        ordered = False
    )
    order_item.quantity -= 1
    if not order_item.quantity:
        order_qs =Order.objects.filter(
        user = request.user,
        ordered = False
        )[0]
        order_qs.items.remove(order_item)
        order_item.delete()

    else:
        order_item.save()
    return redirect('core:order-summary')

def order_done(request, pk):
    order, created  = Order.objects.update_or_create(
        pk = pk,
        defaults = {
        'ordered' : True
        }
    )
    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    messages.info(request, 'Ypur Order has been confirmed')
    return redirect('core:item-list')



