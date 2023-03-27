import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
# Create your views here.


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'client/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'client/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        collections = MenuItem.objects.filter(
            category__name__contains='Collections')
        deliveries = MenuItem.objects.filter(
            category__name__contains='Deliveries')

        # pass into context
        context = {
            'collections': collections,
            'deliveries': deliveries,
        }

        # render the template
        return render(request, 'client/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )

        order.items.add(*item_ids)

        # Send confirmation email
        body = ('Thank you for your order! Your trash will be moving soon. \n '
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }


        return render(request, 'client/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.et(pk=pk)
            order.is_paid = True
            order.save()
            
        return redirect('payment_confirmation.html')

class OrderPayConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        return render(request, 'client/order_pay_confirmation.html')

