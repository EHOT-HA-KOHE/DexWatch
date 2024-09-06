from typing import Any

from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from pairs.models import Pools

class PairView(TemplateView):
    template_name = 'pairs/pair.html'
    # pair_address = 'pair_address'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Pair Info'
        context["pool"] = Pools.objects.get(address=self.kwargs.get('pair_address'))
        return context
    