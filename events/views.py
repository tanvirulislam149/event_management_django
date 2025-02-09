from django.shortcuts import render
from events.forms import EventModelForm, CategoryModelForm
from django.shortcuts import redirect
from django.contrib import messages
from events.models import Event, Category
from django.db.models import Count
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_organizer_or_admin(user):
    return user.groups.filter(name="Organizer").exists() or user.groups.filter(name="Admin").exists()

def is_user(user):
    return user.groups.filter(name="User").exists()


@login_required
# @user_passes_test(is_organizer_or_admin)
def dashboard(request):
    if is_user(request.user):
        users = User.objects.prefetch_related("events").get(id = request.user.id)
        context = {
            "is_user": True,
            "users": users
        }
        return render(request, "event_table.html", context)

    events = Event.objects.select_related("category").annotate(nums_of_participants=Count("participants")).all()
    event_count = Event.objects.aggregate(
        events=Count("id"),
        upcoming = Count("id", filter=Q(date__gt = datetime.now().date())),
        past = Count("id", filter=Q(date__lt = datetime.now().date())),
        todays_count = Count("id", filter=Q(date = datetime.now().date()))
    )
    participant_count = User.objects.all().count()
    category_count = Category.objects.all().count()
    todays_events = Event.objects.filter(date= datetime.now().date())
    
    upcoming = request.GET.get("upcoming")
    past = request.GET.get("past")
    if upcoming:
        events = Event.objects.select_related("category").annotate(nums_of_participants=Count("participants")).filter(date__gt = datetime.now().date())
        print(events)
    elif past:
        events = Event.objects.select_related("category").annotate(nums_of_participants=Count("participants")).filter(date__lt = datetime.now().date())
    else:
        events = Event.objects.select_related("category").annotate(nums_of_participants=Count("participants")).all()
    
    context = {
        "events": events,
        "event_count": event_count,
        "participant_count": participant_count,
        "category_count": category_count,
        "todays_events": todays_events,
        "is_admin": is_admin(request.user),
        "is_organizer": is_organizer_or_admin(request.user),
    }
    return render(request, "event_table.html", context)

# def show_upcoming_events(request):
#     pass

@login_required
@user_passes_test(is_admin, "no_permission")
def show_participant(request):
    participants = User.objects.all()
    context = {
        "participants": participants,
        "is_admin": is_admin(request.user),
        "is_organizer": is_organizer_or_admin(request.user),
    }
    return render(request, "participants.html", context)

@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def show_category(request):
    category = Category.objects.all()
    context = {
        "category": category,
        "is_admin": is_admin(request.user),
        "is_organizer": is_organizer_or_admin(request.user),
    }
    return render(request, "category.html", context)


def details(request, id):
    event = Event.objects.select_related("category").prefetch_related("participants").get(id = id)
    context = {
        "event": event
    }
    return render(request, "details.html", context)

@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def create_event(request, pageId):
    if(request.method == "POST"):
        if pageId == 1:  # 1 => shows create event form
            event_form = EventModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event saved successfully.")
            
        # elif pageId == 2:  # 2 ==> shows create participant form
        #     event_form = ParticipantsModelForm(request.POST)
        #     if event_form.is_valid():
        #         event_form.save()
        #         messages.success(request, "Participant created successfully.")

        elif pageId == 3:
            event_form = CategoryModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Category created successfully.")

        return redirect("create_event", pageId)
        
    else :
        event_form = EventModelForm()
        # Participant_form = ParticipantsModelForm()
        cat_form = CategoryModelForm()
        context = {
            "type": "create",
            "form": event_form if pageId == 1 else cat_form,  # decides which form to render
            "pageId": pageId,
            "is_admin": is_admin(request.user),
            "is_organizer": is_organizer_or_admin(request.user),
        }
        return render(request, "create_event.html", context)

@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def update_event(request, pageId, eventId):
    event = None
    if(request.method == "POST"):
        if pageId == 1:  # 
            event = Event.objects.get(id = eventId)
            event_form = EventModelForm(request.POST, instance = event)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event saved successfully.")
            
        # elif pageId == 2:
        #     event = User.objects.get(id = eventId)
        #     event_form = ParticipantsModelForm(request.POST, instance = event)
        #     if event_form.is_valid():
        #         print(event_form.cleaned_data)
        #         event_form.save()
        #         messages.success(request, "Participant updated successfully.")

        elif pageId == 3:
            event = Category.objects.get(id = eventId)
            event_form = CategoryModelForm(request.POST, instance = event)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Category updated successfully.")

        return redirect("update_event", pageId = pageId, eventId = eventId)
        
    else :
        if pageId == 1:  # 
            event = Event.objects.get(id = eventId)
            
        elif pageId == 2:
            event = User.objects.get(id = eventId)
            
        elif pageId == 3:
            event = Category.objects.get(id = eventId)
            
        
        event_form = EventModelForm(instance = event)
        # Participant_form = ParticipantsModelForm(instance = event)
        cat_form = CategoryModelForm(instance = event)
        context = {
            "type": "update",
            "form": event_form if pageId == 1 else cat_form,
            "pageId": pageId,
            "is_admin": is_admin(request.user),
            "is_organizer": is_organizer_or_admin(request.user),
        }
        return render(request, "create_event.html", context)
        
@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Event deleted")
        return redirect('dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('dashboard')

@login_required
@user_passes_test(is_admin, "no_permission")
def delete_participants(request, id):
    if request.method == "POST":
        event = User.objects.get(id = id)
        event.delete()
        messages.success(request, "Participant deleted")
        return redirect('show_participants')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show_participants')

@login_required
@user_passes_test(is_organizer_or_admin, "no_permission")
def delete_category(request, id):
    if request.method == "POST":
        event = Category.objects.get(id = id)
        event.delete()
        messages.success(request, "Category deleted")
        return redirect('show_category')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show_category')
    

@login_required
def accept_invitation(request, event_id):
    event = Event.objects.get(id = event_id)
    if event.confirm_participants.filter(id = request.user.id).exists():
        return redirect("no_permission")
    else:
        event.confirm_participants.add(request.user)
        return redirect("dashboard")