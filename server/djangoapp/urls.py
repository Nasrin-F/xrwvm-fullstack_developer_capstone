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
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
