from email import message
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views import View

from pairs.models import Pools
from users.models import User
from watchlist.models import PoolList


class CategoriesList(TemplateView):
    template_name = "watchlist/watchlist_categories.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "User`s Lists"
        # context['collections'] = PoolList.objects.filter(user=self.request.user)
        return context


class CategoryPoolList(TemplateView):
    template_name = "watchlist/category_pairs.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pool_list, created = PoolList.objects.get_or_create(
            user=self.request.user, name=kwargs.get("category_name")
        )
        context["pools"] = pool_list.pools.all()
        context["content"] = kwargs.get("category_name").capitalize()
        context["category_name"] = kwargs.get("category_name").capitalize()
        context["is_saving_view"] = True
        return context


class CreateNewCategoryPoolList(View):
    def post(self, request, *args, **kwargs):
        category_name = request.POST.get("category_name")

        if category_name == "":
            collections = render_to_string(
                "watchlist/_categories_list.html", {"request": request}
            )
            return JsonResponse(
                {
                    "message": "Категория не может быть пустой.",
                    "collections": collections,
                }
            )

        user = request.user
        # Логика создания новой категории, если требуется
        category, created = PoolList.objects.get_or_create(
            name=category_name, user=user
        )

        if not created:
            return JsonResponse(
                {"message": f"Категория с именем {category} уже существует."}
            )

        collections = render_to_string(
            "watchlist/_categories_list.html", {"request": request}
        )

        # Формируем данные для ответа
        response_data = {
            "message": f"Категория {category} создана.",
            "collections": collections,
        }

        return JsonResponse(response_data)


class DelCategoryPoolList(View):
    def post(self, request):
        category_name = request.POST.get("category_name")
        user = request.user

        category = PoolList.objects.filter(user=user, name=category_name)
        if not category.exists():
            return JsonResponse(
                {
                    "message": f"Подборка {category_name} не была удалена для пользователя {user.username}, "
                    / "так как ее не существует"
                }
            )

        category.first().delete()

        collections = render_to_string("watchlist/_categories_list.html", {"request": request})

        return JsonResponse(
            {
                "message": f"Подборка {category_name} успешно удалена для пользователя {user.username}",
                "collections": collections
            }
        )


class AddPoolToCategoryPoolList(View):
    def post(self, request):
        pool = Pools.objects.filter(address=request.POST.get("pool_address"))
        if not pool.exists():
            return JsonResponse(
                {"message": f"Пул не был добавлен в подборку, пул не был найден"}
            )

        user_category = PoolList.objects.filter(
            user=self.request.user, name=request.POST.get("collection_name")
        )
        if not user_category.exists():
            return JsonResponse(
                {
                    "message": f"Пул не был добавлен в подборку, у пользователя нет подборки с таким именем"
                }
            )

        pool = pool.first()
        user_category = user_category.first()

        is_pool_in_category = user_category.pools.filter(id=pool.id).exists()
        if is_pool_in_category:
            return JsonResponse({"message": f"Пул уже добавлен в эту подборку"})

        user_category.pools.add(pool)

        response_data = {
            "message": f"Пул успешно добавлен в вашу подборку {user_category.name}"
        }

        return JsonResponse(response_data)


class DelPoolFromCategoryPoolList(View):
    def post(self, request):
        pool_address = request.POST.get('pool_address')
        category_name = request.POST.get('collection_name')
        user = request.user

        pool_list = PoolList.objects.filter(user=user, name=category_name)
        if not pool_list.exists():
            return JsonResponse({'message': 'Этот категория не была найдена'})
        pool_list = pool_list.first()

        pool = Pools.objects.filter(address=pool_address)
        if not pool.exists():
            return JsonResponse({'message': 'Этот пул не был найден'})
        pool = pool.first()

        pool_list.pools.remove(pool)

        pool_url = reverse('pairs:pair_address', kwargs={
            'chain': pool.dex_name.blockchain.name, 
            'pair_address': pool_address
        })

        return JsonResponse(
                {
                    'message': f'Пул {pool_address} был успешно удален из категории {category_name}', 
                    'pool_url': pool_url,
                 }
            )
