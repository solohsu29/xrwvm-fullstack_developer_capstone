from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Path for registration
    path('registration/', views.registration, name='registration'),
    # Path for login
    path('login/', views.login_user, name='login'),
    # Path for logout
    path('logout/', views.logout_request, name='logout'),
    # Path for retrieving car models
        path(route='get_cars', view=views.get_cars, name ='getcars'),
    # Path for retrieving dealerships
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    
    # Path for retrieving dealership details
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # Path for retrieving dealer reviews
        path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    # Path for adding a review
        path(route='add_review', view=views.add_review, name='add_review'),
] 