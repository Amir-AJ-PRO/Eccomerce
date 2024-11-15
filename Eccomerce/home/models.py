from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 , unique=True)

    class Meta:
        ordering : ('name' , )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name 
    

class Product(models.Model):
    category    = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='products')
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200 , unique=True)
    price       = models.IntegerField()
    image       = models.ImageField()
    description = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering : ('neme' , )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home:product_detail' , args=(self.slug,))