from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE


def products_view(request):
    if request.method == "GET":
        product_id = request.GET.get("id")
        if product_id:
            product = DATABASE.get(product_id)
            if product:
                return JsonResponse(product, json_dumps_params={'ensure_ascii': False, 'indent': 4})
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            data = DATABASE
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ


