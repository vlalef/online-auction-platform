from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path('listing/<int:listing_id>/open/', views.open_auction, name='open_auction'),
    path('listing/<int:listing_id>/close/', views.close_auction, name='close_auction'),
    path('place_bid_index/<int:listing_id>/', views.place_bid_index, name='place_bid_index'),
    path('place_bid/<int:listing_id>/', views.place_bid, name='place_bid'),
    path("categories/", views.categories_view, name="categories"),
    path("category/<int:category_id>/", views.category_view, name="category"),
    path("category/create/", views.create_category, name="create_category"),
    path("category/delete/<int:category_id>/", views.delete_category, name="delete_category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path('listing/<int:listing_id>/toggle_watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path("watchlist/remove/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path('add_to_watchlist_index/<int:listing_id>', views.add_to_watchlist_index, name='add_to_watchlist_index'),
    path('add_to_watchlist_detail/<int:listing_id>', views.add_to_watchlist_detail, name='add_to_watchlist_detail'),
]
