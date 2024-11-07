from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Chefs(models.Model):
    name = models.CharField(max_length=100, verbose_name='Oshpaz ismi', blank=True)
    slug = models.SlugField(max_length=100, verbose_name='Oshpaz ismi', unique=True)  
    description = models.TextField(blank=True, verbose_name='Oshpaz haqida')
    image = models.ImageField(upload_to='chefs/', verbose_name='Oshpaz rasmi')
    age = models.IntegerField(default=18, verbose_name='Oshpaz yoshi')
    designation = models.CharField(max_length=75, verbose_name='Lavozimi', blank=True)

    def __str__(self):
        return f"{self.name} ({self.designation})"  

    class Meta:
        verbose_name = 'Oshpaz'
        verbose_name_plural = 'Oshpazlar'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ovqat kategoriyasi nomi')
    description = models.TextField(blank=True, verbose_name='Ovqat kategoriyasi tavsifi')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"  
    
    class Meta:
        verbose_name = 'Ovqat Kategoriyasi'
        verbose_name_plural = 'Ovqat Kategoriyalari'


class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ovqat nomi')
    slug = models.SlugField(max_length=160, unique=True) 
    description = models.TextField(verbose_name='Ovqat haqida')
    image = models.ImageField(upload_to='food/', verbose_name='Ovqat rasmi')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ovqat narxi $')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    discount = models.IntegerField(null=True, blank=True, verbose_name="Chegirma (%)")
    chef = models.ForeignKey(Chefs, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})" 

    class Meta:
        verbose_name = 'Ovqat'
        verbose_name_plural = 'Ovqatlar'


class Review(models.Model):
    text = models.CharField(max_length=75, verbose_name='Izoh matni')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Foydalanuvchi', related_name='reviews')
    full_name = models.CharField(max_length=100, verbose_name='To\'liq ismi')
    rating = models.IntegerField(validators=[
        MinValueValidator(1, "Kamida 1 ta bo'lishi kerak"),
        MaxValueValidator(5, "Eng ko'pi 5 ta bo'lishi kerak")
    ], verbose_name='Bahosi')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Izoh qo'shilgan vaqti")
    profession = models.CharField(max_length=100, null=True, verbose_name='Kasbi')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='reviews', verbose_name='Taom')

    def __str__(self):
        return f"{self.full_name} | {self.text[:50]}..."  

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def get_range(self):
        return range(1, 6) 
