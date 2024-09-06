from django.urls import path

from pairs.views import PairView

app_name = 'pairs'

urlpatterns = [
    path('<str:chain>/<str:pair_address>/', PairView.as_view(), name='pair_address')
]
