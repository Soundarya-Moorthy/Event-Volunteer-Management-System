from datetime import date, datetime, time
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from accounts.models import Registration    
from .models import Volunteer, ContactMessage
from django.contrib import messages
from django.shortcuts import render
from .forms import VolunteerForm
from .forms import ContactForm
from accounts.models import HomePageEvent
from accounts.models import AllEvents  

def enrich_events(events):
    for event in events:
        event.tag_list = event.tags.split(',') if event.tags else []
        event.role_list = event.roles.split(',') if event.roles else []

def register_view(request, event_id):
    event = get_object_or_404(AllEvents, id=event_id)
    #event.role_list = event.roles.split(',') if event.roles else []
    #event.tag_list = event.tags.split(',') if event.tags else []
    roles = event.role_list
    tags = event.tag_list

    if request.method == 'POST':
        Registration.objects.create(
            event=event,
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            role=request.POST['role']
        )
        messages.success(request, 'Registration successful!')
        return redirect('submit_registration', event_id=event.id)
    
    return render(request, 'events/register.html', {'event': event, 'roles': roles,
        'tags': tags})

def index_view(request):
    # Show only homepage events
    events = HomePageEvent.objects.filter(show_on_homepage=True).order_by('-date')
    return render(request, 'accounts/index.html', {'events': events})

def event_view(request):
    today = date.today()
    upcoming = AllEvents.objects.filter(date__gte=today).order_by('date')
    past = AllEvents.objects.filter(date__lt=today).order_by('-date')
    all_events = AllEvents.objects.all().order_by('-date')

    context = {
        'upcoming': upcoming,
        'past': past,
        'all_events': all_events,
        'today': today
    }
    return render(request, 'events/event.html', context)

def allevents_view(request):
    today = datetime.today().date()
    query = request.GET.get('search', '')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    start_time_filter = request.GET.get('startTime')
    selected_roles = request.GET.getlist('roles')

    events = AllEvents.objects.all()

    if query:
        events = events.filter(title__icontains=query)

    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    if start_time_filter:
     if start_time_filter == 'morning':
        events = events.filter(time__gte='09:00', time__lt='12:00')
     elif start_time_filter == 'afternoon':
        events = events.filter(time__gte='12:00', time__lt='17:00')
     elif start_time_filter == 'evening':
        events = events.filter(time__gte='17:00', time__lt='21:00')

    if selected_roles:
       filtered_events = [event for event in events if any(role in event.role_list for role in selected_roles)]
       event_ids = [event.id for event in filtered_events]
       events = AllEvents.objects.filter(id__in=event_ids)

    upcoming = events.filter(date__gte=today)
    past = events.filter(date__lt=today)
    all_events = events

    role_options = ['Photography', 'Information Desk', 'Registration Assistance', 'Others', 'Social Media']

    context = {
        'upcoming': upcoming,
        'past': past,
        'all_events': all_events,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'start_time_filter': start_time_filter,
        'selected_roles': selected_roles,
        'role_options': role_options,
        'today': today,
    }

    return render(request, 'events/event.html', context)

def admin_dashboard(request):
    homepage_events = HomePageEvent.objects.filter(show_on_homepage=True).order_by('-date')
    allevents = AllEvents.objects.all().order_by('-date')
    volunteers = Volunteer.objects.all()
    registrations = Registration.objects.select_related('event').order_by('-registered_at')
    messages = ContactMessage.objects.all().order_by('-submitted_at')
    

    context = {
        'events': homepage_events,
        'allevents': allevents,    
        'volunteers': volunteers,
        'registrations': registrations, 
        'messages': messages
    
    }
    return render(request, 'accounts/admin_dashboard.html', context)

def volunteer_registration(request):
    success = False
    if request.method == 'POST':
        preferred_days = ','.join(request.POST.getlist('preferred_days'))
        preferred_time_slots = ','.join(request.POST.getlist('preferred_time_slots'))

        Volunteer.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            dob=request.POST.get('dob'),
            gender=request.POST.get('gender'),
            address=request.POST.get('address'),
            languages=request.POST.get('languages'),
            current_status=request.POST.get('current_status'),
            preferred_days=preferred_days,
            preferred_time_slots=preferred_time_slots,
            specific_dates=request.POST.get('specific_dates'),
            has_experience=request.POST.get('has_experience') == 'yes',
            experience_details=request.POST.get('experience_details'),
        )
        success = True

    return render(request, 'accounts/Volunteer_section.html', {'success': success})

def contact_view(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm() 
    else:
        form = ContactForm()

    return render(request, 'accounts/Contact_us.html', {'form': form, 'success': success})
