from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from .models import Chefs, Category, Food, Review
from django.db.models import Q
from collections import defaultdict
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Home(View):
    def get(self, request):
        context = {
            'foods': Food.objects.all(),
            'chefs': Chefs.objects.all(),
            'categories': Category.objects.all(),
            'reviews': Review.objects.all(),
        }
        return render(request, 'index.html', context)

    def post(self, request):
        full_name = request.POST.get("full_name")
        profession = request.POST.get("profession")
        text = request.POST.get("text")
        rate = request.POST.get("rate")

        if full_name and profession and text and rate:
            try:
                rate = int(rate)
                if rate < 1 or rate > 5:
                    return redirect('home')  
                if request.user.is_authenticated:
                    Review.objects.create(
                        text=text,
                        rate=rate,
                        user=request.user,
                        full_name=full_name,
                        profession=profession,
                    )
                return redirect('home')
            except Exception as e:
                logger.error(f"Error creating review: {e}")
                return redirect('home')
        return redirect('home')


class MenuView(ListView):
    model = Food
    template_name = 'menu.html'
    context_object_name = 'foods'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.kwargs.get('category_name')
        search_query = self.request.GET.get('q')

        if category_name:
            queryset = queryset.filter(category__name=category_name)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_count = defaultdict(int)

        for food in Food.objects.all():
            category_count[food.category.name] += 1

        context['category_count'] = category_count
        return context


class MenuByCategoryView(ListView):
    model = Food
    template_name = 'menu.html'
    context_object_name = 'foods'

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        search_query = self.request.GET.get('q')
        queryset = Food.objects.filter(category__name=category_name)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs.get('category_name')

        context['category_count'] = Food.objects.filter(category__name=category_name).count()
        return context
