from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('postComment', views.postComment, name="postComment"),
    path('login', views.signin, name='login'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('post-detail/<slug>', views.post_detail, name="post_detail"),
    path('about-us', views.about_us, name="about_us"),
    path('contact-us', views.contact_us, name="contact_us"),
    path('search', views.search, name='search'),
]