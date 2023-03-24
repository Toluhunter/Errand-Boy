from django.urls import path

from . import views

urlpatterns = [
    path("category/<uuid:id>/", views.ListCategoryView.as_view(), name="categories"),
    path("add-category/", views.AddCategoryView.as_view(), name="add-category"),
    path("all/", views.ListProductView.as_view(), name="products"),
    path("manage-product/<str:id>/",
         views.ManageProductView.as_view(), name="manage-product"),
    path("add-product/", views.CreateProductView.as_view(), name="add-product"),
    path("delete-category/<uuid:id>/", views.DeleteCategoryView.as_view(),
         name="delete-category"),
    path("delete-product/<str:id>/",
         views.DeleteProductView.as_view(), name="delete-product"),
    path("myproducts/", views.FetchFoodServiceProductView.as_view(),
         name="fetch-products")
]
