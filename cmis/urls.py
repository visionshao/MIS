from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r"^$", views.index, name="index"),格式如左
    url(r'index/', views.index, name="index"),
    url(r'menuManagement/', views.menuManagement, name="menuManagement"),
    url(r'appointManagement/', views.appointManagement, name="appointManagement"),
    url(r'purchaseManagement/', views.purchaseManagement, name="purchaseManagement"),
    url(r'ordersManagement/', views.ordersManagement, name="ordersManagement"),
    url(r'repertoryManagement/', views.repertoryManagement, name="repertoryManagement"),
    url(r'saleManagement/', views.saleManagement, name="saleManagement"),
    url(r'getPredictResult/', views.getPredictResult, name="getPredictResult"),
    url(r'getRepertoryResult/', views.getRepertoryResult, name="getRepertoryResult"),
    url(r'getSingleRepertoryResult/', views.getSingleRepertoryResult, name="getSingleRepertoryResult"),
    url(r'getMenuResult/', views.getMenuResult, name="getMenuResult"),
    url(r'getSingleMenuResult/', views.getSingleMenuResult, name="getSingleMenuResult"),
    url(r'getSaleResult/', views.getSaleResult, name="getSaleResult"),
    url(r'getSingleSaleResult/', views.getSingleSaleResult, name="getSingleSaleResult"),
    url(r'getOrdersResult/', views.getOrdersResult, name="getOrdersResult")
]