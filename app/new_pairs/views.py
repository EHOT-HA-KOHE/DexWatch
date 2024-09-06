import json
from typing import Any

from django.views.generic import TemplateView
from django.shortcuts import render

from app.settings import BASE_DIR
from pairs.models import Blockchains, DexNames, Pools

class NewPairsView(TemplateView):
    template_name = 'new_pairs/new_pairs.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Pairs'
        
        chain = self.kwargs.get('chain')
        context['content'] = chain.capitalize()

        # with open(f'{BASE_DIR}/new_pairs/temp_token_data.json', 'r') as file:
        #     tokens = json.load(file)

        if chain == 'all':
            tokens = Pools.objects.all()
        else:
            blockchain = Blockchains.objects.filter(name=chain).exists()
            if blockchain:
                blockchain = Blockchains.objects.get(name=chain)
                dex = DexNames.objects.filter(blockchain=blockchain)
                tokens = Pools.objects.filter(dex_name__in=dex)

            else:
                self.template_name = 'new_pairs/not_working_blockchain.html'
                tokens = []


        context['pools'] = tokens

        return context
