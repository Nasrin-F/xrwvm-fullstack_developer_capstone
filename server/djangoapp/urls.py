from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView

app_name = 'djangoapp'

urlpatterns = [
    # Authentication and User Management
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration, name='register'),

    # Car Data and Reviews
    path('get_cars/', views.get_cars, name='get_cars'),
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_details'),
    path('add_review/', views.add_review, name='add_review'),

    # Dealerships
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    # Optional: Serve an HTML page (if needed)
    # path('', TemplateView.as_view(template_name='index.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
