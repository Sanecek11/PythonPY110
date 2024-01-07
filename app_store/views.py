from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE.get(product_id)  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product["quantity"] = quantity# 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product[
                "price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            products.append(product)# 3. добавьте product в список products
        return render(request, "store/cart.html", context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def products_view(request):
    if request.method == "GET":
        if product_id := request.GET.get("id"):
            if data := DATABASE.get(product_id):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")
            # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"):  # Если в параметрах есть 'ordering'
            if request.GET.get("reverse").lower() == 'true':  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
                data = filtering_category(DATABASE, category_key, ordering_key, False)
        else:
            data = filtering_category(DATABASE, category_key)
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        return render(request,
                      'store/shop.html',
                      context={"products": DATABASE.values()})


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


