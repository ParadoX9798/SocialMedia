from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("register/", views.user_register, name="user_register"),
    path("logout/", views.user_logout, name="user_logout"),
    path('dashboard/<int:id>/', views.user_dashboard, name="user_dashboard"),
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("email_login", views.email_login, name="email_login"),
    path("verify/<str:user_email>/<int:rand_num>/", views.verify, name="verify"),
    path("follow", views.follow, name="follow"),
    path("unfoloow", views.unfollow, name="unfollow"),

]
