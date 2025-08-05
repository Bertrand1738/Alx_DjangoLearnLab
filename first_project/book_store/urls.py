from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.products, name="products"),
    path("secure-products/", views.secure_products, name="secure_products"),
    path("add-product/", views.add_product, name="add_product"),
    path("edit-product/<int:product_id>/", views.edit_product, name="edit_product"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile_view, name="profile"),
    path("manage-inventory/", views.manage_inventory, name="manage_inventory"),
    path("set-prices/", views.set_prices, name="set_prices"),
    path("featured-products/", views.feature_products, name="feature_products"),
    path("delete-product/<int:product_id>/", views.delete_product, name="delete_product"),
]