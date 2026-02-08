from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.utils import timezone
from accounts.models import HomePageEvent
from accounts.models import Registration
from accounts.models import AllEvents 
from events.models import Volunteer, ContactMessage
# ----------------------
# Authentication Views
# ----------------------

def admin_login_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        # Hardcoded username as superuser
        user = authenticate(username='SoundaryaMoorthy', password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin password")
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        login_type = request.POST.get("login_type")  # 'volunteer' or 'admin'

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on login type
            if login_type == "volunteer":
                return redirect('event_list')  # Goes to event/event.html
            elif login_type == "admin":
                return redirect('admin_dashboard')  # Or 'index' if homepage
            else:
                return redirect('index')  # Fallback
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# ----------------------
# Frontend Views
# ----------------------

def index_view(request):
    featured_events = HomePageEvent.objects.filter(show_on_homepage=True).order_by('-date')[:4]
    return render(request, 'accounts/index.html',  {'featured_events': featured_events})

def contact_us(request):
    return render(request, 'accounts/Contact_us.html')

def event_highlights(request):
    events = HomePageEvent.objects.filter(show_on_homepage=True).order_by('-date')
    return render(request, 'accounts/Event_highlights.html', {'events': events})

def past_event(request):
    return render(request, 'accounts/Past_event.html')

def volunteer_section(request):
    return render(request, 'accounts/Volunteer_section.html')

def about_us(request):
    return render(request, 'accounts/About_us.html')

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

def allevents(request):
    today = datetime.today().date()

    # Optional filters from GET params
    query = request.GET.get('search', '')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    start_time_filter = request.GET.get('startTime')
    selected_roles = request.GET.getlist('roles')

    events = AllEvents.objects.all()

    # Apply filters
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

    # Categorize events
    
    upcoming = events.filter(date__gte=today)
    past = events.filter(date__lt=today)
    all_events = events

    # Role options for sidebar
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

def register_event(request, event_id):
    if request.method == "POST":
        event = AllEvents.objects.get(id=event_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')

        Registration.objects.create(
            event=event,
            name=name,
            email=email,
            phone=phone,
            role=role
        )
        messages.success(request, "Registered successfully!")
        return redirect('event_list')

# ----------------------
# Admin Dashboard Views
# ----------------------
@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_registration(request, reg_id):
    try:
        reg = Registration.objects.get(id=reg_id)
        reg.delete()
        messages.success(request, 'Registration deleted successfully.')
    except Registration.DoesNotExist:
        messages.error(request, 'Registration not found.')
    return redirect('admin_dashboard')

@login_required(login_url='login')
def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')
        date = request.POST['date']
        HomePageEvent.objects.create(title=title, description=description, image=image, date=date, 
        show_on_homepage=True)
        messages.success(request, 'Event added successfully.')
        return redirect('admin_dashboard')
    return render(request, 'accounts/add_event.html')

@login_required(login_url='login')
def edit_event(request, event_id):
    event = get_object_or_404(HomePageEvent, id=event_id)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        image = request.FILES.get('image')

        if title:
            event.title = title
        if description:
            event.description = description
        if date:
            event.date = date
        if image:
            event.image = image

        event.save()
        messages.success(request, "Homepage Event updated successfully.")
        return redirect('admin_dashboard')

    return render(request, 'accounts/edit_event.html', {'event': event})

@login_required(login_url='login')
def delete_event(request, event_id):
    event = get_object_or_404(HomePageEvent, id=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Homepage Event deleted successfully.')
        return redirect('admin_dashboard')

    return render(request, 'accounts/delete_event.html', {'object': event})

@login_required(login_url='login')
def add_allevent(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        roles = request.POST.get('roles')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')

        AllEvents.objects.create(
            title=title,
            description=description,
            date=date,
            time=time,
            location=location,
            roles=roles,
            tags=tags,
            image=image
        )
        messages.success(request, "Event added successfully.")
        return redirect('admin_dashboard')

    return render(request, 'accounts/add.html')

@login_required(login_url='login')
def edit_allevent(request, event_id):
    try:
        event = AllEvents.objects.get(id=event_id)
    except AllEvents.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('admin_dashboard')

    if request.method == "POST":
        event.title = request.POST.get('title') or event.title
        event.description = request.POST.get('description') or event.description
        event.date = request.POST.get('date') or event.date
        event.time = request.POST.get('time') or event.time
        event.location = request.POST.get('location') or event.location
        event.roles = request.POST.get('roles') or event.roles
        event.tags = request.POST.get('tags') or event.tags

        if 'image' in request.FILES:
            event.image = request.FILES['image']

        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect('admin_dashboard')

    return render(request, 'accounts/edit.html', {'event': event})

@login_required(login_url='login')
def delete_allevent(request, event_id):
    try:
        event = AllEvents.objects.get(id=event_id)
    except AllEvents.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('admin_dashboard')

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('admin_dashboard')

    return render(request, 'accounts/delete.html', {'event': event})
