from django.urls import path
from . import views
from .views import contact_view

urlpatterns = [
    path('', views.index_view, name='event_index'),
    path('', views.allevents_view, name='event_list'),
    path('event/<int:event_id>/', views.event_view, name='event_view'),
    path('register/<int:event_id>/', views.register_view, name='submit_registration'),
    path('volunteer/', views.volunteer_registration, name='volunteer_registration'),
    path('contact/', views.contact_view, name='contact_view'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
