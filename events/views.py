from django.shortcuts import render
from events.forms import EventModelForm, ParticipantsModelForm, CategoryModelForm
from django.shortcuts import redirect
from django.contrib import messages
from events.models import Event, Participant, Category

# Create your views here.
def home(request):
    return render(request, "home.html")

def dashboard(request):
    return render(request, "dashboard.html")

def create_event(request, pageId):
    if(request.method == "POST"):
        if pageId == 1:  # 1 => shows create event form
            event_form = EventModelForm(request.POST)
            print("check 1")
            if event_form.is_valid():
                event_form.save()
                print("check 2")
                messages.success(request, "Event saved successfully.")
            
        elif pageId == 2:  # 2 ==> shows create participant form
            event_form = ParticipantsModelForm(request.POST)
            if event_form.is_valid():
                print(event_form.cleaned_data)
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
                messages.success(request, "Participant created successfully.")

        elif pageId == 3:
            event = Category.objects.get(id = eventId)
            event_form = CategoryModelForm(request.POST, instance = event)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Category created successfully.")

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
        
