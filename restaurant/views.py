from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView

from .models import Chefs, Category, Food, Review
from django.db.models import Q
from collections import defaultdict
import logging
from django.contrib import messages


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
                    messages.error(request, "Reyting 1 dan 5 gacha bo'lishi kerak.")
                    return redirect('home')
                if request.user.is_authenticated:
                    s = Review.objects.create(
                        text=text,
                        rate=rate,
                        user=request.user,
                        full_name=full_name,
                        profession=profession,
                    )
                    s.save()
                    messages.success(request, "Izoh muvaffaqiyatli qo'shildi!")  
                return redirect('home')
            except Exception as e:
                messages.error(request, "Izoh qo'shishda xatolik yuz berdi.")
                return redirect('home')
        messages.error(request, "Barcha maydonlarni to'ldiring.")
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

class Booking(View):
    def get(self, request):
        context = {
            'foods': Food.objects.all(),
        }


        return render(request, 'index.html', context)
    

class Detail(View):
    def get(self, request, pk):
        food = get_object_or_404(Food, pk=pk) 
        reviews = Review.objects.filter(food=food)
        
        context = {
            'food': food,
            'reviews': reviews,
        }
        return render(request, 'food_detail.html', context)
    

class FoodDetailView(DetailView):
    model = Food
    template_name = 'food_detail.html'
    context_object_name = 'food'