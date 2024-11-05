from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Chefs(models.Model):
    name = models.CharField(max_length=100, verbose_name='oshpaz ismi', blank=True)
    slug = models.SlugField(max_length=100, verbose_name = 'oshpaz ismi')
    description = models.TextField(blank=True, verbose_name='oshpaz haqida')
    image = models.ImageField(upload_to='chefs/', verbose_name='oshpaz rasmi')
    age = models.IntegerField(default=18, verbose_name='ochpazni yoshi')
    designation = models.CharField(max_length=75, verbose_name='lavozmi', blank=True)

    

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = ('Oshpaz')
        verbose_name_plural = 'Oshpazlar'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='ovqat kategoriyasi nomi')
    description = models.TextField(blank=True, verbose_name='ovqat kategoriyasi tavsifi')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ('Ovqat kategiriyasi')
        verbose_name_plural = 'Ovqat kategiriyalari'

class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name='ovqat nomi')
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(verbose_name='ovqat haqida')
    image = models.ImageField(upload_to='food/', verbose_name='ovqat rasmi')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ovqat narxi $')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')  
    discount = models.IntegerField(null=True, blank=True, verbose_name="Chegirma (%)")
    chef = models.ForeignKey(Chefs, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('Ovqat')
        verbose_name_plural = 'Ovqatlar'


class Review(models.Model):
    text = models.CharField(max_length=75, verbose_name = 'izoh matni')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='foydalanuvchi', related_name='reviews')
    full_name = models.CharField(max_length=100, verbose_name='To\'liq ismi')
    rating  = models.IntegerField(validators=[
        MinValueValidator(1 , "kamida 1 ta bo'lishi kerak"),
        MaxValueValidator(5, "eng ko'pi 5 ta bo'lishi kerak")
    ], verbose_name='bahosi')
    created = models.DateTimeField(auto_now_add=True, verbose_name="izoh qo'shilgan vaqti")
    profession = models.CharField(max_length=100, null=True, verbose_name='kasbi')


    def __str__(self):
        return f"{self.full_name} | {self.text[:100]}"

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def get_range(self):
        return [1, 2, 3, 4, 5]