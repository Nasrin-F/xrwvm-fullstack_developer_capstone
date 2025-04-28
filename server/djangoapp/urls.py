# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView


app_name = 'djangoapp'
urlpatterns = [

    path('get_cars/', views.get_cars, name='get_cars'),  # Path for getting car data
    path('logout/', views.logout_request, name='logout'),  # Path for logging out
    path('register/', views.registration, name='register'),  # Path for registering a user
    path('login/', views.login_user, name='login'),  # Path for logging in
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
