from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .models import *
from . import tasks
from django.contrib import messages
from bucket import bucket
from utils import IsAdminUserMixin

# Create your views here.
class HomeIndexView(View):
    def get(self , request):
        products = Product.objects.filter(available=True)
        self.context = {
            'products' : products ,
        }
        return render(request , 'home/home.html' , context=self.context)
    
class ProductDetailView(View):
    def get(self , request , slug):
        product = get_object_or_404(Product , slug=slug)
        return render(request , 'home/productdetail.html' , {'product' : product})
    
class BucketView(IsAdminUserMixin , View):
    def get(self , request):
        objects = tasks.all_bucket_objects_task()
        return render(request , 'home/bucket.html' , {'objects':objects})
    

class DeleteObjBucketView(IsAdminUserMixin , View):
    def get(self , request , key):
        tasks.delete_object_task.delay(key)
        #bucket.delete_object(key=key)
        messages.success(request , 'youre object will be delete soon' , 'success')
        return redirect('home:bucket')
    


class DownloadObjBucketView(IsAdminUserMixin , View):
    def get(self , request , key):
        tasks.download_obj_task.delay(key)
        #bucket.download_object(key=key)
        messages.success(request , 'youre object will be download soon' , 'success')
        return redirect('home:bucket')