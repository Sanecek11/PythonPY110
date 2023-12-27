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


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'app_store/products/{page}.html', encoding="utf-8") as file:
                        content = file.read()
                    return HttpResponse(content)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'app_store/products/{data["html"]}.html', encoding="utf-8") as f:
                    content_1 = f.read()
                return HttpResponse(content_1)
        return HttpResponse(status=404)


