from django.urls import path

from watchlist import views


app_name = 'watchlist'


urlpatterns = [
    path('categories/', views.CategoriesList.as_view(), name='categories'),
    path('categories/<str:category_name>', views.CategoryPoolList.as_view(), name='category_pools'),
    path('add_to_category/', views.AddPoolToCategoryPoolList.as_view(), name='add_to_category'),
    path('del_from_category/', views.DelPoolFromCategoryPoolList.as_view(), name='del_from_category'),
    path('create_category/', views.CreateNewCategoryPoolList.as_view(), name='create_category'),
    path('del_category/', views.DelCategoryPoolList.as_view(), name='del_category'),
]
