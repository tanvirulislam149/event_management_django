from django.shortcuts import render
from events.forms import EventModelForm, ParticipantsModelForm, CategoryModelForm
from django.shortcuts import redirect
from django.contrib import messages
from events.models import Event, Participant, Category
from django.db.models import Count
from django.db.models import Q
from datetime import datetime

# Create your views here.

def dashboard(request):
    events = Event.objects.select_related("category").prefetch_related("participants").annotate(nums_of_participants=Count("participants")).all()
    event_count = Event.objects.aggregate(
        events=Count("id"),
        upcoming = Count("id", filter=Q(date__gt = datetime.now().date())),
        past = Count("id", filter=Q(date__lt = datetime.now().date())),
        todays_count = Count("id", filter=Q(date = datetime.now().date()))
    )
    participant_count = Participant.objects.all().count()
    category_count = Category.objects.all().count()
    todays_events = Event.objects.filter(date= datetime.now().date())
    
    upcoming = request.GET.get("upcoming")
    past = request.GET.get("past")
    if upcoming:
        events = Event.objects.select_related("category").prefetch_related("participants").annotate(nums_of_participants=Count("participants" )).filter(date__gt = datetime.now().date())
        print(events)
    elif past:
        events = Event.objects.select_related("category").prefetch_related("participants").annotate(nums_of_participants=Count("participants")).filter(date__lt = datetime.now().date())
    else:
        events = Event.objects.select_related("category").prefetch_related("participants").annotate(nums_of_participants=Count("participants")).all()
    
    context = {
        "events": events,
        "event_count": event_count,
        "participant_count": participant_count,
        "category_count": category_count,
        "todays_events": todays_events
    }
    return render(request, "event_table.html", context)

def show_upcoming_events(request):
    pass

def show_participant(request):
    participants = Participant.objects.all()
    context = {
        "participants": participants
    }
    return render(request, "participants.html", context)

def show_category(request):
    category = Category.objects.all()
    context = {
        "category": category
    }
    return render(request, "category.html", context)

def details(request, id):
    event = Event.objects.get(id = id)
    context = {
        "event": event
    }
    return render(request, "details.html", context)


def create_event(request, pageId):
    if(request.method == "POST"):
        if pageId == 1:  # 1 => shows create event form
            event_form = EventModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                print("check 2")
                messages.success(request, "Event saved successfully.")
            
        elif pageId == 2:  # 2 ==> shows create participant form
            event_form = ParticipantsModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Participant created successfully.")

        elif pageId == 3:
            event_form = CategoryModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Category created successfully.")

        return redirect("create_event", pageId)
        
    else :
        event_form = EventModelForm()
        Participant_form = ParticipantsModelForm()
        cat_form = CategoryModelForm()
        context = {
            "type": "create",
            "form": event_form if pageId == 1 else Participant_form if pageId == 2 else cat_form,
            "pageId": pageId
        }
        return render(request, "create_event.html", context)
        
def update_event(request, pageId, eventId):
    event = None
    if(request.method == "POST"):
        if pageId == 1:  # 
            event = Event.objects.get(id = eventId)
            event_form = EventModelForm(request.POST, instance = event)
            print("check 1")
            if event_form.is_valid():
                event_form.save()
                print("check 2")
                messages.success(request, "Event saved successfully.")
            
        elif pageId == 2:
            event = Participant.objects.get(id = eventId)
            event_form = ParticipantsModelForm(request.POST, instance = event)
            if event_form.is_valid():
                print(event_form.cleaned_data)
                event_form.save()
                messages.success(request, "Participant updated successfully.")

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
            event = Participant.objects.get(id = eventId)
            
        elif pageId == 3:
            event = Category.objects.get(id = eventId)
            
        print(event)
        event_form = EventModelForm(instance = event)
        Participant_form = ParticipantsModelForm(instance = event)
        cat_form = CategoryModelForm(instance = event)
        context = {
            "type": "update",
            "form": event_form if pageId == 1 else Participant_form if pageId == 2 else cat_form,
            "pageId": pageId
        }
        return render(request, "create_event.html", context)
        
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Event deleted")
        return redirect('dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('dashboard')
    
def delete_participants(request, id):
    if request.method == "POST":
        event = Participant.objects.get(id = id)
        event.delete()
        messages.success(request, "Participant deleted")
        return redirect('show_participants')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show_participants')

def delete_category(request, id):
    if request.method == "POST":
        event = Category.objects.get(id = id)
        event.delete()
        messages.success(request, "Category deleted")
        return redirect('show_category')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('show_category')