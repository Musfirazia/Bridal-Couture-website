from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name="ShopHome"),
    path("postad/", views.postad,name="PostAd"),
    path("product/<int:myid>", views.productview,name="productview"),
    path("quickform/", views.quickform,name="quickform"),
    path("category/<slug:category>", views.categoryview,name="bridaldresses"),
    path("contact/", views.contact,name="contact"),
    path("about/", views.about,name="AboutUs"),
    path("login/", views.login,name="Login"),
    path("signup/", views.userdetails,name="userdetails"),
    path("signin/", views.signin,name="signin"),
    path("checkout/", views.checkout,name="checkout"),
    path("stripe/",views.stripee,name="stripee"),
    path("vendors/<slug:vendorname>",views.vendorsearch,name="vendorsearch"),
    path("search/",views.search,name="search"),

]