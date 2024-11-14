from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeIndexView.as_view() , name='home' ),
    path('product/<slug:slug>/', ProductDetailView.as_view() , name='product_detail' ),
    path('bucket/', BucketView.as_view() , name='bucket' ),
    path('bucket/delete_obj/<key>/', DeleteObjBucketView.as_view() , name='delete_obj_bucket' ),
    path('bucket/download_obj/<key>/', DownloadObjBucketView.as_view() , name='download_obj_bucket' ),
]