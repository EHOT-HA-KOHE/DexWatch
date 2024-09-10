from typing import Any

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView

from pairs.models import Pools
from pairs.utils import q_search


class PairView(TemplateView):
    template_name = 'pairs/pair.html'
    # pair_address = 'pair_address'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Pair Info'
        context["pool"] = Pools.objects.get(address=self.kwargs.get('pair_address'))
        return context
    

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')

        query_results = q_search(query)

        q_results = render_to_string(
            "pairs/search_result.html", {"query_results": query_results}
        )

        # Формируем данные для ответа
        response_data = {
            "q_results": q_results,
            "message": "Вот результаты поиска",
        }

        return JsonResponse(response_data)
