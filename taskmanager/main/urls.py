from django.contrib import admin
from django.urls import path
from . import views
from .views import profile
from .views import LogoutView
from .views import ChangeUserInfoView
from .views import PasswordChangeView
from .views import DeleteUserView
from .views import by_rubric
from .views import detail
from .views import profile_bb_add
from .views import profile_bb_delete
from .views import profile_bb_change

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.index, name='home'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/change/<int:pk>/', profile_bb_change, name='profile_bb_change'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name='profile_bb_delete'),




]
