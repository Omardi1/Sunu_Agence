from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import  Count, Q
from django.views.generic.base import View
from django.db.models import Sum
from django.db.models import F
from django.core.paginator import Paginator
from Agence.models import Suite, Cart, Order, Category
from .forms import SuiteForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import SuiteSerializer
from rest_framework.decorators import api_view



# Create your views here.



@login_required(login_url='login')
def index(request):
    all_suite = Suite.objects.all()
    p = Paginator(Suite.objects.all(), 7)
    page = request.GET.get('page')
    suites = p.get_page(page) 
    return render(request, 'Agence/index.html',  context={"all_suite": all_suite, 'suites': suites})


@login_required(login_url='login')
def suite_detail(request, slug):
    suite= get_object_or_404(Suite, slug=slug)
    return render(request, 'Agence/suite_detail.html', context={"suite": suite})


class SuiteList(View):
    template_name = 'Agence/suite_list.html'

    def get(self, request):
        suites = Suite.objects.all()
        categories = Category.objects.all()
        q = request.GET.get("q")
        request.session["nom"] = "Agence"
        request.session.get("nom")
        del request.session["nom"]
        if q:
            suites = Suite.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )
        return render(request, self.template_name, {"suites": suites, "categories": categories, })

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        suites = Suite.objects.filter(city__contains=searched)
        return render(request, 'Agence/search.html', {'searched': searched,
                                                      'suites': suites})
    else:
        return render(request, 'search.html', {})
    
     
     
@login_required(login_url='login')     
def add_to_cart(request, slug):
    user = request.user
    suite = get_object_or_404(Suite, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                 suite=suite)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity +=1 
        order.save()

        return redirect('cart')
    return redirect(reverse("suite", kwargs={"slug": slug}))       



@login_required(login_url='login')
def cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    total_price = Order.objects.filter(user=user, cart=cart).annotate(total_price=F('quantity') * F('suite__price')).aggregate(total=Sum('total_price'))
    return render(request, 'Agence/cart.html', {'cart': cart, 'total_price': total_price['total']})



@login_required(login_url='login')
def validate_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    for order in cart.orders.all():
        order.ordered = True
        order.ordered_date = timezone.now()
        order.save()
    cart.orders.clear()
    return redirect('order_summary')



@login_required(login_url='login')
def order_summary(request):
    user = request.user
    orders = Order.objects.filter(user=user, ordered=True)
    total_price = orders.aggregate(total=Sum('suite__price'))
    return render(request, 'Agence/order_summary.html', {'orders': orders, 'total_price': total_price['total']})



@login_required(login_url='login')
def delete_cart(request):
    if cart :=request.user.cart:
        cart.delete()
    return redirect('index') 




@login_required(login_url='login')
def cart_detail(request):
    # Récupère le panier de l'utilisateur connecté ou crée un nouveau panier
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Calculer le montant total du panier
    total = 0
    for order in cart.orders.all():
        if order.ordered == False:
            total += order.quantity * order.suite.price
    
    # Afficher les détails du panier
    context = {
        'cart': cart,
        'total': total,
    }
    return render(request, 'Agence/cart_detail.html', context)



@login_required(login_url='login')
def about(request):
    return render(request, 'Agence/about.html')



@login_required(login_url='login')
def contact(request):
    return render(request, 'Agence/contact.html')



@login_required(login_url='login')
def thank_you(request, total_price):
    return render(request, 'Agence/thank_you.html', {'total_price': total_price})



@login_required(login_url='login')
def new_suite(request):
    if request.method == "POST":
        form = SuiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = SuiteForm()
    context = {"form": form}
    return render(request, "Agence/new_suite.html", context)


@login_required(login_url='login')
def update_suite(request, slug):
    suite = Suite.objects.get(slug=slug)
    if request.method == "POST":
        form = SuiteForm(request.POST, instance=suite)
        if form.is_valid():
            form.save()
            return redirect("suite", slug=suite.slug)
    else:
        form = SuiteForm(instance=suite)
    return render(request, "Agence/update_suite.html", {"form": form, "suite": suite}) 



@login_required(login_url='login')
def delete_suite(request, slug):
    suite = Suite.objects.get(slug=slug)
    if request.method == 'POST':
        suite.delete()
        return redirect('suite_list')
    return render(request, 'Agence/delete_suite.html', {'suite': suite})



def dashboard(request):
    num_available_suites = Suite.objects.filter(available=True).count()
    total_num_suites = Suite.objects.count()
    total_revenue = Suite.objects.filter(available=True).aggregate(Sum('price'))['price__sum']
    cities = Suite.objects.filter(available=True).values('city').annotate(num_suites=Count('id'))
    return render(request, 'Agence/dashboard.html', {
        'num_available_suites': num_available_suites,
        'total_num_suites': total_num_suites,
        'total_revenue': total_revenue,
        'cities': cities,
    })


class SuiteListe(APIView):
    
        def get(self, request):
         suite = Suite.objects.all()
         serializer = SuiteSerializer(suite, many=True)
         return Response(serializer.data)

@api_view()
def suite_details(request, id):
    suite = get_object_or_404(Suite, pk=id)
    serializer = SuiteSerializer(suite)
    return Response(serializer.data)     