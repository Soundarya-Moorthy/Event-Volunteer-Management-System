from django.urls import path
from . import views
from events.views import event_view

urlpatterns = [
    path('', views.index_view, name='index'), 
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about_us, name='about_us'),
    path('highlights/', views.event_highlights, name='event_highlights'),
    path('past-events/', views.past_event, name='past_event'),
    path('volunteer/', views.volunteer_section, name='volunteer_section'), # Public landing page
    path('event/', views.allevents, name='event_list'),  # Volunteer dashboard
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('register/<int:event_id>/', views.register_event, name='submit_registration'),  # Registration
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('delete-registration/<int:reg_id>/', views.delete_registration, name='delete_registration'),

    # HomeEvents management
    path('add-event/', views.add_event, name='add_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

     # AllEvents management
    path('add-allevent/', views.add_allevent, name='add_allevent'),
    path('edit-allevent/<int:event_id>/', views.edit_allevent, name='edit_allevent'),
    path('delete-allevent/<int:event_id>/', views.delete_allevent, name='delete_allevent'),
]
