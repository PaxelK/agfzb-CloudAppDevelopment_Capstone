from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path('about/', views.about, name='about'),
    # path for contact us view
    path('contact/', views.contact, name='contact'),
    # path for registration
    path('registration_request/', views.registration_request, name='registration'),
    # path for login
    path('login_request/', views.login_request, name='login'),
    # path for logout
    path('logout_request/', views.logout_request, name='logout'),
    path('dealer/<int:id>/add_review/', views.add_review, name='add_review'),
    path(route='', view=views.get_dealerships, name='index'),
    path(route='dealer/<int:id>/', view=views.get_dealer_details, name='dealer_details')
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)