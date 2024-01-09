from django.shortcuts import render, redirect
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth import get_user
import json
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from app_store.models import DATABASE
# Create your views here.


@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        with open('wishlist.json', 'r') as f:
            data = json.load(f)[current_user]['products']

        products = [DATABASE.get(product_id) for product_id in data]  # Список продуктов

        return render(request, 'wishlist/wishlist.html', context={"products": products})


def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"})
        return JsonResponse({"answer": "Неудачное добавление в избранное"}, status=404)


@login_required(login_url='login:login_view')
def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"})

        return JsonResponse({"answer": "Неудачное удаление из избранного"}, status=404)


@login_required(login_url='login:login_view')
def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username
        wishlist_users = view_in_wishlist(request)
        data = wishlist_users.get(current_user, {})
        if data:
            return JsonResponse(data)

        return JsonResponse({"answer": "Пользователь не авторизирован"}, status=404)


def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)
        if result:
            return redirect("app_wishlist:wishlist_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")


